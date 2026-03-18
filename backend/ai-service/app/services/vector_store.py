"""Qdrant vector store for device search using LangChain."""

from pydantic import SecretStr
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.http.models import (
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
    Range,
    SearchParams,
    VectorParams,
)
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from app.schemas.device import (
    DeviceSpecifications,
    DeviceTraits,
)

from app.config import settings


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
    ) -> None:
        """Add a device to the vector store. Text is name + tags for embedding."""

        metadata = {
            "name": name,
            "price": price,
            "traits": traits if traits else {},
            "specifications": specifications if specifications else {},
            "key_features": key_features if key_features else [],
        }
        doc = Document(page_content=short_description, metadata=metadata)
        vectorstore = self._get_vectorstore()
        vectorstore.add_documents([doc])

    def search(
        self,
        prompt: str,
        k: int = 5,
        *,
        max_price: float | None,
        traits: DeviceTraits,
    ) -> list[dict]:
        """Find devices by prompt using similarity search."""
        vectorstore = self._get_vectorstore()

        filter_conditions: list[FieldCondition] = []

        # 1. Fallback Price Logic
        effective_max_price = float(max_price or traits.price or 0);

        # 2. Filter Conditions
        specs_dict = traits.model_dump(exclude_none=True)

        form_factor: str | None = traits.form_factor if traits.form_factor else None

        if form_factor and form_factor not in ["unknown", "any", ""]:
            
            filter_conditions.append(
                FieldCondition(
                    key="metadata.traits.form_factor",
                    match=MatchValue(value=form_factor)
                )
        )

        for key, value in specs_dict.items():
            if value not in [None, "unknown", "any", ""] and key != "price" and key != "form_factor":
                filter_conditions.append(
                FieldCondition(
                    key=f"metadata.traits.{key}",
                    match=MatchValue(value=value),
                )
            )

        if effective_max_price > 0:
            filter_conditions.append(
                FieldCondition(
                    key="metadata.price",
                    range=Range(lte=effective_max_price),
                )
            )

        filter: Filter = Filter(must=list(filter_conditions))

        # 3. Search Execution
        docs = vectorstore.similarity_search(
            prompt,
            k=k,
            filter=filter if filter_conditions else None,
            search_params=SearchParams(hnsw_ef=128),
            score_threshold=0.5,
        )

        devices = []

        for d in docs:
            devices.append({
                "name": d.metadata.get("name", ""),
                "price": float(d.metadata.get("price") or 0),
                "category": d.metadata.get("traits", "").get("category", ""),
                "short_description": d.page_content,
                "specifications": d.metadata.get("specifications", {}),
                "key_features": d.metadata.get("key_features", []),
            })

            print(devices, "devices")
        
        return devices


vector_store_service = VectorStoreService()
