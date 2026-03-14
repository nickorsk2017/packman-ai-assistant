"""Qdrant vector store for device search using LangChain."""

from pydantic import SecretStr
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue, Range
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA

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
        tags: list[str],
        price: float | None = None,
        category: str | None = None,
    ) -> None:
        """Add a device to the vector store. Text is name + tags for embedding."""
        text = f"{name} {' '.join(tags)}".strip()
        metadata = {
            "name": name,
            "tags": tags,
            "price": price,
            "category": category or "",
        }
        doc = Document(page_content=text, metadata=metadata)
        vectorstore = self._get_vectorstore()
        vectorstore.add_documents([doc])

    def search(
        self,
        prompt: str,
        k: int = 5,
        *,
        category: str | None = None,
        max_price: float | None = None,
    ) -> list[dict]:
        """Find devices by prompt using similarity search. Returns list of metadata dicts.

        Optional filters:
        - category: only devices with matching category metadata
        - max_price: only devices with price <= max_price
        """
        vectorstore = self._get_vectorstore()

        qdrant_filter: Filter | None = None
        conditions: list[FieldCondition] = []

        if category:
            conditions.append(
                FieldCondition(
                    key="metadata.category",
                    match=MatchValue(value=category),
                )
            )

        if max_price is not None:
            conditions.append(
                FieldCondition(
                    key="metadata.price",
                    range=Range(lte=max_price),
                )
            )
        
        if conditions:
            qdrant_filter = Filter(must=list        (conditions))  # type: ignore[arg-type]


        docs = vectorstore.similarity_search(prompt, k=k, filter=qdrant_filter)
        
        return [
            {
                "name": d.metadata.get("name", ""),
                "tags": d.metadata.get("tags", []),
                "price": d.metadata.get("price"),
                "category": d.metadata.get("category", ""),
            }
            for d in docs
        ]

    def ask(self, query: str, k: int = 2) -> str:
        """Answer a natural-language question about devices using RetrievalQA (Qdrant + LLM)."""
        vectorstore = self._get_vectorstore()
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        llm = ChatOpenAI(
            model="gpt-5-mini", 
            temperature=0,
            api_key=SecretStr(settings.openai_api_key)
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
        )
        out = qa_chain.invoke({"query": query})
        return out.get("result", "") if isinstance(out, dict) else str(out)


vector_store_service = VectorStoreService()
