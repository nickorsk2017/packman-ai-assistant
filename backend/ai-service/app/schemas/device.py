from pydantic import BaseModel


class DeviceDescriptionResponse(BaseModel):
    name: str
    description: str


class DeviceInfoResponse(BaseModel):
    name: str
    description: str
    specifications: str


class DeviceAddRequest(BaseModel):
    """Payload to add a device to the vector database (FAISS)."""

    name: str
    description: str | None = None
    price: float | None = None
    category: str | None = None


class DeviceIndexResponse(BaseModel):
    """Response after indexing a device."""

    name: str
    tags: list[str]
    indexed: bool = True


class DeviceSearchResult(BaseModel):
    """One device from search results."""

    name: str
    tags: list[str]
    price: float | None = None
    category: str = ""


class DeviceSearchResponse(BaseModel):
    """Devices found by prompt/tags in vector DB."""

    prompt: str
    devices: list[DeviceSearchResult]


class DeviceAskResponse(BaseModel):
    """LLM answer from RetrievalQA over device catalog."""

    query: str
    answer: str
