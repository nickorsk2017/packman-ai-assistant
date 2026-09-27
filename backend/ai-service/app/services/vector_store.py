"""Qdrant vector store for device search using LangChain."""

import re
import uuid
from typing import Any

from pydantic import SecretStr
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.http.models import (
    Distance,
    Filter,
    FieldCondition,
    MatchAny,
    MatchValue,
    Range,
    SearchParams,
    VectorParams,
)
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from app.schemas.device import (
    DeviceSpecifications,
    DeviceTraits,
)

from app.config import settings

IGNORED_TRAIT_VALUES = (None, "unknown", "any", "")
EXACT_FILTER_TRAITS = ("brand", "os", "category")
PHONE_FORM_FACTORS = ["phone", "foldable"]


def normalize_traits(traits: dict[str, Any]) -> dict[str, Any]:
    """Lowercase string traits so filters match regardless of LLM casing."""
    return {k: v.strip().lower() if isinstance(v, str) else v for k, v in traits.items()}


def device_point_id(name: str) -> str:
    """Stable point id per device name, so re-indexing overwrites instead of duplicating."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"packman-device:{name.strip().lower()}"))


def strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or "")).strip()


def build_page_content(
    name: str,
    short_description: str,
    traits: dict[str, Any],
    specifications: dict[str, Any],
    key_features: list[str],
) -> str:
    """Plain text used for the embedding: name, facts first, marketing text last."""
    lines = [name]
    display_count = traits.get("display_count")
    if display_count:
        lines.append(
            "Screens: 2, dual screen" if display_count >= 2 else "Screens: 1, single screen"
        )
    if key_features:
        lines.append("Key features: " + ", ".join(key_features))
    specs = [f"{k}: {v}" for k, v in specifications.items() if v not in IGNORED_TRAIT_VALUES]
    if specs:
        lines.append("Specifications: " + "; ".join(specs))
    trait_values = [
        f"{k}: {v}" for k, v in traits.items()
        if v not in IGNORED_TRAIT_VALUES and k != "display_count"
    ]
    if trait_values:
        lines.append("Traits: " + "; ".join(trait_values))
    description = strip_html(short_description)
    if description:
        lines.append(description)
    return "\n".join(lines)


class VectorStoreService:
    """Manages Qdrant index for devices: add devices, search by prompt."""

    def __init__(self) -> None:
        self._embeddings: OpenAIEmbeddings | None = None
        self._client: QdrantClient | None = None
        self._vectorstore: QdrantVectorStore | None = None

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        if self._embeddings is None:
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set")
            self._embeddings = OpenAIEmbeddings(api_key=SecretStr(settings.openai_api_key))
        return self._embeddings

    @property
    def client(self) -> QdrantClient:
        """Shared Qdrant client. Uses qdrant_url if set (server/dashboard), else embedded at qdrant_path."""
        if self._client is None:
            if settings.qdrant_url:
                self._client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key,
                )
            else:
                self._client = QdrantClient(path=settings.qdrant_path)
        return self._client

    def _ensure_collection(self) -> None:
        """Create the Qdrant collection if it does not already exist."""
        client = self.client
        name = settings.qdrant_collection
        try:
            client.get_collection(collection_name=name)
            return
        except ResponseHandlingException as e:
            if "Connection refused" in str(e) or "Errno 61" in str(e):
                url = settings.qdrant_url or "localhost:6333"
                raise ValueError(
                    f"Qdrant server at {url} is not running. Start it with: uv run packman-run-qdrant"
                ) from e
            raise
        except Exception:
            # Collection is missing; create it based on embedding dimensionality.
            dim = len(self.embeddings.embed_query("dimension_probe"))
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def _get_vectorstore(self) -> QdrantVectorStore:
        """Return a Qdrant vector store, creating the collection if needed."""
        if self._vectorstore is None:
            self._ensure_collection()
            self._vectorstore = QdrantVectorStore(
                client=self.client,
                collection_name=settings.qdrant_collection,
                embedding=self.embeddings,
            )
        return self._vectorstore

    def add_device(
        self,
        name: str,
        short_description: str,
        traits: DeviceTraits | None = None,
        specifications: DeviceSpecifications | None = None,
        key_features: list[str] | None = None,
        price: float | None = None,
        description: str | None = None,
        sources: list[str] | None = None,
    ) -> None:
        """Add or overwrite a device in the vector store."""
        traits_dict = normalize_traits(traits.model_dump(exclude_none=True)) if traits else {}
        specs_dict = specifications.model_dump(exclude_none=True) if specifications else {}
        features = key_features or []

        metadata = {
            "name": name,
            "price": price,
            "description": description or "",
            "short_description": short_description,
            "traits": traits_dict,
            "specifications": specs_dict,
            "key_features": features,
            "sources": sources or [],
        }
        doc = Document(
            page_content=build_page_content(name, short_description, traits_dict, specs_dict, features),
            metadata=metadata,
        )
        vectorstore = self._get_vectorstore()
        vectorstore.add_documents([doc], ids=[device_point_id(name)])

    def search(
        self,
        prompt: str,
        k: int = 5,
        *,
        max_price: float | None,
        traits: DeviceTraits,
    ) -> list[dict]:
        """Find candidate devices by prompt: hard filters on traits, then vector similarity."""
        vectorstore = self._get_vectorstore()

        query_traits = normalize_traits(traits.model_dump(exclude_none=True))

        price_conditions: list[FieldCondition] = []
        effective_max_price = float(max_price or 0)
        if effective_max_price > 0:
            price_conditions.append(
                FieldCondition(key="metadata.price", range=Range(lte=effective_max_price))
            )

        trait_conditions: list[FieldCondition] = []
        for key in EXACT_FILTER_TRAITS:
            value = query_traits.get(key)
            if value not in IGNORED_TRAIT_VALUES:
                trait_conditions.append(
                    FieldCondition(key=f"metadata.traits.{key}", match=MatchValue(value=value))
                )

        form_factor = query_traits.get("form_factor")
        if form_factor not in IGNORED_TRAIT_VALUES:
            allowed = PHONE_FORM_FACTORS if form_factor in PHONE_FORM_FACTORS else [form_factor]
            trait_conditions.append(
                FieldCondition(key="metadata.traits.form_factor", match=MatchAny(any=allowed))
            )

        display_count = query_traits.get("display_count")
        if display_count and display_count >= 2:
            trait_conditions.append(
                FieldCondition(key="metadata.traits.display_count", range=Range(gte=display_count))
            )

        def run(conditions: list[FieldCondition]):
            return vectorstore.similarity_search_with_score(
                prompt,
                k=k,
                filter=Filter(must=conditions) if conditions else None,
                search_params=SearchParams(hnsw_ef=128),
            )

        results = run(price_conditions + trait_conditions)
        if not results and trait_conditions:
            print(f"No candidates with trait filters {query_traits}, retrying with price filter only")
            results = run(price_conditions)

        devices = []
        for doc, score in results:
            meta = doc.metadata
            traits_meta = meta.get("traits") or {}
            devices.append({
                "name": meta.get("name", ""),
                "price": float(meta.get("price") or 0),
                "category": traits_meta.get("category", ""),
                "short_description": meta.get("short_description") or doc.page_content,
                "traits": traits_meta,
                "specifications": meta.get("specifications") or {},
                "key_features": meta.get("key_features") or [],
                "score": score,
            })
        return devices


vector_store_service = VectorStoreService()
