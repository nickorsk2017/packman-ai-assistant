"""FAISS vector store for device search using LangChain."""

from pathlib import Path

from pydantic import SecretStr
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA

from app.config import settings


class VectorStoreService:
    """Manages FAISS index for devices: add devices, search by prompt."""

    def __init__(self) -> None:
        self._embeddings: OpenAIEmbeddings | None = None
        self._vectorstore: FAISS | None = None
        self._index_path = Path(settings.faiss_index_path)

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        if self._embeddings is None:
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set")
            self._embeddings = OpenAIEmbeddings(api_key=SecretStr(settings.openai_api_key))
        return self._embeddings

    def _load(self) -> FAISS | None:
        """Load existing FAISS index from disk. Returns None if not found."""
        if not self._index_path.exists():
            return None
        try:
            return FAISS.load_local(
                str(self._index_path),
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        except Exception:
            return None

    def _save(self, vectorstore: FAISS) -> None:
        """Persist FAISS index to disk."""
        self._index_path.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(str(self._index_path))

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

        existing = self._load()
        if existing is not None:
            existing.add_documents([doc])
            self._save(existing)
        else:
            vectorstore = FAISS.from_documents(
                [doc],
                self.embeddings,
            )
            self._save(vectorstore)

    def search(self, prompt: str, k: int = 5) -> list[dict]:
        """Find devices by prompt using similarity search. Returns list of metadata dicts."""
        vectorstore = self._load()
        if vectorstore is None:
            return []
        docs = vectorstore.similarity_search(prompt, k=k)
        
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
        """Answer a natural-language question about devices using RetrievalQA (FAISS + LLM)."""
        vectorstore = self._load()
        if vectorstore is None:
            return "No devices in the catalog yet. Add devices first to search."
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
