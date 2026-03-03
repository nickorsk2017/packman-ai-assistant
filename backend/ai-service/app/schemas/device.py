from pydantic import BaseModel


class DeviceDescriptionResponse(BaseModel):
    name: str
    description: str


class DeviceSpecificationsResponse(BaseModel):
    name: str
    specifications: str


class DeviceInfoResponse(BaseModel):
    name: str
    description: str
    specifications: str
