from pydantic import BaseModel


class DeviceDescriptionResponse(BaseModel):
    name: str
    description: str


class DeviceInfoResponse(BaseModel):
    name: str
    description: str
    traits: str


class DeviceTraits(BaseModel):
    """Extracted traites from device description: os, category, brand."""

    os: str | None = None
    category: str | None = None
    model: str | None = None
    brand: str | None = None
    price: float | None = None
    condition: str | None = None
    cost_range: str | None = None
    storage_capacity: str | None = None
    battery: str | None = None
    screen_size: str | None = None
    form_factor: str | None = None


class DeviceSpecifications(BaseModel):
    """Extracted specifications from device description: os, category, brand."""
    brand: str | None = None
    model: str | None = None
    os: str | None = None
    storage_capacity: str | None = None
    screen_size: str | None = None
    battery_capacity: str | None = None
    form_factor: str | None = None
    camera: str | None = None
    processor: str | None = None
    ram: str | None = None
    storage: str | None = None
    display: str | None = None
    battery_life: str | None = None

class DeviceTraitsAndSpecifications(BaseModel):
    """Extracted traits and specifications from device description: os, category, brand."""
    traits: DeviceTraits | None = None
    specifications: DeviceSpecifications | None = None
    key_features: list[str] | None = None


class DeviceAddRequest(BaseModel):
    """Payload to add a device to the vector database."""

    name: str
    description: str
    price: float


class DeviceIndexResponse(BaseModel):
    """Response after indexing a device."""

    name: str
    indexed: bool = True
    traits: DeviceTraits | None = None
    specifications: DeviceSpecifications | None = None
    short_description: str | None = None
    key_features: list[str] | None = None


class DeviceSearchResult(BaseModel):
    """One device from search results."""

    name: str
    short_description: str | None = None
    price: float | None = None
    category: str = ""
    specifications: DeviceSpecifications | None = None
    key_features: list[str] | None = None


class DeviceSearchResponse(BaseModel):
    """Devices found by prompt/tags in vector DB."""

    prompt: str
    devices: list[DeviceSearchResult]


class DeviceAskResponse(BaseModel):
    """LLM answer from RetrievalQA over device catalog."""

    query: str
    answer: str
