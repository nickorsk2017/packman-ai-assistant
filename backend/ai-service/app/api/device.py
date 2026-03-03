from fastapi import APIRouter, HTTPException, Query

from app.schemas.device import (
    DeviceDescriptionResponse,
    DeviceSpecificationsResponse,
    DeviceInfoResponse,
)
from app.services.device_service import device_service

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


@router.get("/specifications", response_model=DeviceSpecificationsResponse)
def get_device_specifications(
    name: str = Query(..., min_length=1, description="Device or product name"),
) -> DeviceSpecificationsResponse:
    """Get technical specifications of a device by its name (OpenAI)."""
    try:
        return device_service.get_specifications(name)
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
