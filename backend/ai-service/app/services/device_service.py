import dirtyjson

from openai import OpenAI

from app.config import settings
from app.schemas.device import (
    DeviceDescriptionResponse,
    DeviceInfoResponse,
    DeviceTraits,
    DeviceTraitsAndSpecifications,
)

from app.prompts.device_prompts import (
    KEY_FEATURES_DEVICE_FIELDS,
    SPECIFICATIONS_FIELDS_DEVICE,
    TRAITS_FIELDS_DEVICE,
    GET_DEVICE_INFO_PROMPT,
    GET_TRAITS_BY_DEVICE_NAME_PROMPT,
    GET_DEVICE_TRAITS_BY_USER_REQUEST_PROMPT,
    GET_SHORT_DEVICE_DESCRIPTION_PROMPT,
)


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
                {"role": "system", "content": GET_DEVICE_INFO_PROMPT},
                {"role": "user", "content": name.strip() or "Unknown device"},
            ]
        )
        description = (
            (response.choices[0].message.content if response.choices else "") or ""
        ).strip()
        return DeviceDescriptionResponse(name=name, description=description)

    def get_info(self, name: str) -> DeviceInfoResponse:
        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": GET_DEVICE_INFO_PROMPT},
                {"role": "user", "content": name.strip() or "Unknown device"},
            ]
        )
        text = (
            (response.choices[0].message.content if response.choices else "") or ""
        ).strip()
        description = ""
        traits = ""

        if "DESCRIPTION:" in text and "SPECIFICATIONS:" in text:
            parts = text.split("SPECIFICATIONS:", 1)
            desc_part = parts[0].replace("DESCRIPTION:", "").strip()
            description = desc_part.strip()
            traits = parts[1].strip() if len(parts) > 1 else ""
        else:
            description = text
        return DeviceInfoResponse(
            name=name,
            description=description,
            traits=traits,
        )

    def get_short_description(
        self,
        name: str,
        description: str | None = None,
        price: float | None = None,
    ) -> str:
        """Get searchable tags for a device using OpenAI. Includes seller price when provided."""
        user_content = name.strip() or "Unknown device"
        if description and description.strip():
            user_content = f"{user_content}\n\nDescription: {description.strip()}"
        if price is not None:
            user_content = f"{user_content}\n\nSeller price: {price} USD"
        response = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": GET_SHORT_DEVICE_DESCRIPTION_PROMPT},
                {"role": "user", "content": user_content},
            ],
        )
        raw = response.choices[0].message.content if response.choices else ""
        text = (raw or "").strip()
        if not text:
            return name
        
        return text

    def get_device_specs_by_name(self, name: str) -> DeviceTraitsAndSpecifications:
        """Get device params by name in JSON format: os, category, brand..."""
        if not (name or name.strip()):
            return DeviceTraitsAndSpecifications()

        specifications_prompt: str = GET_TRAITS_BY_DEVICE_NAME_PROMPT.format(
            traits_fields=TRAITS_FIELDS_DEVICE,
            specifications_fields=SPECIFICATIONS_FIELDS_DEVICE,
            key_features_device_fields=KEY_FEATURES_DEVICE_FIELDS
        )

        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": specifications_prompt},
                {"role": "user", "content": name.strip()},
            ],
        )

        completion_result = response.choices[0].message.content if response.choices else "{}";

        if not completion_result:
            return DeviceTraitsAndSpecifications()
        try:
            data = dirtyjson.loads(completion_result) or {}
            if not isinstance(data, dict):
                return DeviceTraitsAndSpecifications()

            return DeviceTraitsAndSpecifications.model_validate(data)
          
        except (dirtyjson.Error, TypeError, ValueError) as error:
            print(f"Error occurred: {error}")
       
            return DeviceTraitsAndSpecifications()

    def get_specifications_by_user_prompt(self, user_prompt: str) -> DeviceTraits:
        """Get device params by user prompt in JSON format: os, category, brand..."""
        user_prompt = user_prompt.strip()

        if not (user_prompt):
            return DeviceTraits()

        specifications_prompt = GET_DEVICE_TRAITS_BY_USER_REQUEST_PROMPT.format(traits_fields=TRAITS_FIELDS_DEVICE)

        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": specifications_prompt},
                {"role": "user", "content": user_prompt.strip()},
            ],
        )
        
        completion_result = response.choices[0].message.content if response.choices else "{}";

        if not completion_result:
            return DeviceTraits()
        try:
            data = dirtyjson.loads(completion_result) or {}

            if not isinstance(data, dict):
                return DeviceTraits()

            return DeviceTraits.model_validate(data)
        except (dirtyjson.Error, TypeError, ValueError) as error:
            print(f"Error occurred: {error}")
            print("Error: ", dirtyjson.Error, TypeError)
            return DeviceTraits()


device_service = DeviceService()
