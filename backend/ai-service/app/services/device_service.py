from openai import OpenAI

from app.config import settings
from app.schemas.device import (
    DeviceDescriptionResponse,
    DeviceSpecificationsResponse,
    DeviceInfoResponse,
)

from app.prompts.device_prompts import SPECS_PROMPT, INFO_PROMPT, TAGS_PROMPT


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
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": INFO_PROMPT},
                {"role": "user", "content": name.strip() or "Unknown device"},
            ]
        )
        description = (
            response.choices[0].message.content if response.choices else ""
        ).strip()
        return DeviceDescriptionResponse(name=name, description=description)

    def get_info(self, name: str) -> DeviceInfoResponse:
        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": INFO_PROMPT},
                {"role": "user", "content": name.strip() or "Unknown device"},
            ]
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

    def get_tags(self, name: str, description: str | None = None) -> list[str]:
        """Get searchable tags for a device using OpenAI."""
        user_content = name.strip() or "Unknown device"
        if description and description.strip():
            user_content = f"{user_content}\n\nDescription: {description.strip()}"
        response = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": TAGS_PROMPT},
                {"role": "user", "content": user_content},
            ],
        )
        text = (
            response.choices[0].message.content if response.choices else ""
        ).strip()
        if not text:
            return [name]
        tags = [t.strip().replace(" ", "_") for t in text.split(",") if t.strip()]
        return tags if tags else [name]


device_service = DeviceService()
