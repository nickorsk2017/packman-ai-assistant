from fastapi import APIRouter, HTTPException, Query

from app.schemas.device import (
    DeviceDescriptionResponse,
    DeviceInfoResponse,
    DeviceAddRequest,
    DeviceIndexResponse,
    DeviceSearchResponse,
    DeviceSearchResult,
    DeviceAskResponse,
    DeviceTraits,
    DeviceTraitsAndSpecifications,
)
from app.services.device_service import device_service
from app.services.vector_store import vector_store_service

router = APIRouter(prefix="/device", tags=["device"])

SEARCH_CANDIDATES_MULTIPLIER = 4
SEARCH_CANDIDATES_MAX = 40


@router.get("/description", response_model=DeviceDescriptionResponse)
def get_device_description(
    name: str = Query(..., min_length=1, description="Device name"),
) -> DeviceDescriptionResponse:
    """Get a short description of a device by its name (OpenAI)."""
    try:
        return device_service.get_description(name)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/info", response_model=DeviceInfoResponse)
def get_device_info(
    name: str = Query(..., min_length=1, description="Device name"),
) -> DeviceInfoResponse:
    """Get both description and traits for a device by its name (OpenAI)."""
    try:
        return device_service.get_info(name)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/index", response_model=DeviceIndexResponse)
def index_device(body: DeviceAddRequest) -> DeviceIndexResponse:
    """Add or overwrite a device in the Qdrant vector store. OpenAI generates traits from name/description."""
    try:
        description, sources = device_service.resolve_description(body.name, body.description)
        device_traits_and_specifications: DeviceTraitsAndSpecifications = device_service.get_device_specs_by_name(
            name=body.name,
            description=description,
        )
        short_description: str = device_service.get_short_description(
            body.name, description, body.price, specs=device_traits_and_specifications
        )

        traits = device_traits_and_specifications.traits
        specifications = device_traits_and_specifications.specifications
        key_features = device_traits_and_specifications.key_features

        vector_store_service.add_device(
            name=body.name,
            short_description=short_description,
            price=body.price,
            description=description,
            sources=sources,
            traits=traits,
            specifications=specifications,
            key_features=key_features,
        )
        return DeviceIndexResponse(name=body.name, short_description=short_description, indexed=True, traits=traits, specifications=specifications, key_features=key_features)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/search", response_model=DeviceSearchResponse)
def search_devices(
    prompt: str = Query(..., min_length=1),
    k: int = Query(5, ge=1, le=20, description="Max number of results"),
    max_price: float | None = Query(
        None, ge=0, description="Optional maximum seller price (USD)"
    )
) -> DeviceSearchResponse:
    """Find devices: LLM extracts traits, Qdrant filters and ranks candidates, LLM keeps only matching ones."""
    try:
        traits: DeviceTraits = device_service.get_specifications_by_user_prompt(user_prompt=prompt)

        candidates = vector_store_service.search(
            prompt,
            k=min(k * SEARCH_CANDIDATES_MULTIPLIER, SEARCH_CANDIDATES_MAX),
            max_price=max_price or traits.price or None,
            traits=traits,
        )
        results = device_service.rerank_devices(prompt, candidates)[:k]

        devices = [
            DeviceSearchResult(
                name=r["name"],
                price=r.get("price"),
                category=r.get("category") or "",
                short_description=r.get("short_description") or "",
                specifications=r.get("specifications", {}),
                key_features=r.get("key_features", []),
            )
            for r in results
        ]

        return DeviceSearchResponse(prompt=prompt, devices=devices)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
