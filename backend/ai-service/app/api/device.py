from fastapi import APIRouter, HTTPException, Query

from app.schemas.device import (
    DeviceDescriptionResponse,
    DeviceSpecificationsResponse,
    DeviceInfoResponse,
    DeviceAddRequest,
    DeviceIndexResponse,
    DeviceSearchResponse,
    DeviceSearchResult,
    DeviceAskResponse,
)
from app.services.device_service import device_service
from app.services.vector_store import vector_store_service

router = APIRouter(prefix="/device", tags=["device"])


@router.get("/description", response_model=DeviceDescriptionResponse)
def get_device_description(
    name: str = Query(..., min_length=1, description="Device or product name"),
) -> DeviceDescriptionResponse:
    """Get a short description of a device by its name (OpenAI)."""
    try:
        return device_service.get_description(name)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/info", response_model=DeviceInfoResponse)
def get_device_info(
    name: str = Query(..., min_length=1, description="Device or product name"),
) -> DeviceInfoResponse:
    """Get both description and specifications for a device by its name (OpenAI)."""
    try:
        return device_service.get_info(name)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/index", response_model=DeviceIndexResponse)
def index_device(body: DeviceAddRequest) -> DeviceIndexResponse:
    """Add a device to the FAISS vector database. OpenAI generates tags from name/description."""
    try:
        tags = device_service.get_tags(body.name, body.description, body.price)
        if body.price is not None:
            price_tag = f"price_{int(body.price)}"
            if price_tag not in tags:
                tags = [*tags, price_tag]
        vector_store_service.add_device(
            name=body.name,
            tags=tags,
            price=body.price,
            category=body.category,
        )
        return DeviceIndexResponse(name=body.name, tags=tags, indexed=True)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/search", response_model=DeviceSearchResponse)
def search_devices(
    prompt: str = Query(..., min_length=1, description="Search prompt or tags"),
    k: int = Query(5, ge=1, le=20, description="Max number of results"),
) -> DeviceSearchResponse:
    """Find devices by prompt and tags using FAISS vector similarity search."""
    try:
        results = vector_store_service.search(prompt, k=k)
        devices = [
            DeviceSearchResult(
                name=r["name"],
                tags=r["tags"],
                price=r.get("price"),
                category=r.get("category") or "",
            )
            for r in results
        ]
        return DeviceSearchResponse(prompt=prompt, devices=devices)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/ask", response_model=DeviceAskResponse)
def ask_devices(
    q: str = Query(..., min_length=1, description="Natural language question about devices"),
    k: int = Query(2, ge=1, le=10, description="Number of documents to retrieve"),
) -> DeviceAskResponse:
    """Find devices and get an LLM answer using LangChain RetrievalQA over FAISS."""
    try:
        answer = vector_store_service.ask(q, k=k)
        return DeviceAskResponse(query=q, answer=answer)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
