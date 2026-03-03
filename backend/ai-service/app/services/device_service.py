from openai import OpenAI

from app.config import settings
from app.schemas.device import (
    DeviceDescriptionResponse,
    DeviceSpecificationsResponse,
    DeviceInfoResponse,
)

DESCRIPTION_PROMPT = """You are a product expert. Given a device or product name, provide a clear, concise description (2-4 sentences) suitable for a product catalog. Focus on what the product is, key use cases, and main audience. Only output the description, no preamble."""

SPECS_PROMPT = """You are a product expert. Given a device or product name, provide technical specifications in a structured format (e.g. key specs as bullet points or short lines: display, processor, storage, battery, etc.). Be factual and concise. Only output the specifications, no preamble."""

INFO_PROMPT = """You are a product expert. Given a device or product name, provide:
1. A short description (2-4 sentences).
2. Technical specifications (bullet points or short lines).

Format your response as:
DESCRIPTION:
<description text>

SPECIFICATIONS:
<specifications text>

Only output the above, no other preamble."""


class DeviceService:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set")
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def get_description(self, name: str) -> DeviceDescriptionResponse:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": DESCRIPTION_PROMPT},
                {"role": "user", "content": name.strip() or "Unknown device"},
            ],
            max_tokens=500,
        )
        description = (
            response.choices[0].message.content if response.choices else ""
        ).strip()
        return DeviceDescriptionResponse(name=name, description=description)

    def get_specifications(self, name: str) -> DeviceSpecificationsResponse:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SPECS_PROMPT},
                {"role": "user", "content": name.strip() or "Unknown device"},
            ],
            max_tokens=800,
        )
        specifications = (
            response.choices[0].message.content if response.choices else ""
        ).strip()
        return DeviceSpecificationsResponse(name=name, specifications=specifications)

    def get_info(self, name: str) -> DeviceInfoResponse:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": INFO_PROMPT},
                {"role": "user", "content": name.strip() or "Unknown device"},
            ],
            max_tokens=1000,
        )
        text = (
            response.choices[0].message.content if response.choices else ""
        ).strip()
        description = ""
        specifications = ""
        if "DESCRIPTION:" in text and "SPECIFICATIONS:" in text:
            parts = text.split("SPECIFICATIONS:", 1)
            desc_part = parts[0].replace("DESCRIPTION:", "").strip()
            description = desc_part.strip()
            specifications = parts[1].strip() if len(parts) > 1 else ""
        else:
            description = text
        return DeviceInfoResponse(
            name=name,
            description=description,
            specifications=specifications,
        )


device_service = DeviceService()
