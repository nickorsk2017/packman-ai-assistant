import json

import dirtyjson

from openai import OpenAI, OpenAIError

from app.config import settings
from app.schemas.device import (
    DeviceDescriptionResponse,
    DeviceInfoResponse,
    DeviceResearch,
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
    RERANK_DEVICES_PROMPT,
    RESEARCH_DEVICE_PROMPT,
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

    def research_device(self, name: str) -> DeviceResearch:
        """Find facts about the device on the web (OpenAI web_search tool)."""
        name = name.strip()
        if not name:
            return DeviceResearch()
        try:
            response = self.client.responses.create(
                model=settings.research_model,
                tools=[{"type": "web_search"}],
                instructions=RESEARCH_DEVICE_PROMPT,
                input=name,
            )
        except OpenAIError as error:
            print(f"Device research failed for {name!r}: {error}")
            return DeviceResearch()

        text = (response.output_text or "").strip()
        lines = text.splitlines()
        first = lines[0].strip().lower() if lines else ""
        facts = "\n".join(lines[1:]).strip() if first.startswith("found:") else text
        found = bool(facts) and not first.startswith("found: no")

        sources: list[str] = []
        for item in response.output:
            if item.type != "message":
                continue
            for content in item.content:
                for annotation in getattr(content, "annotations", None) or []:
                    url = getattr(annotation, "url", None)
                    if annotation.type == "url_citation" and url and url not in sources:
                        sources.append(url)

        return DeviceResearch(found=found, facts=facts if found else "", sources=sources)

    def resolve_description(self, name: str, description: str | None) -> tuple[str, list[str]]:
        """Seller description if provided, otherwise facts from the web. Returns (description, sources)."""
        if description and description.strip():
            return description.strip(), []
        research = self.research_device(name)
        return research.facts, research.sources

    def get_description(self, name: str) -> DeviceDescriptionResponse:
        """Description for the Add Device form: facts about the device from the web."""
        research = self.research_device(name)
        return DeviceDescriptionResponse(
            name=name,
            description=research.facts,
            found=research.found,
            sources=research.sources,
        )

    def get_info(self, name: str) -> DeviceInfoResponse:
        response = self.client.chat.completions.create(
            model="gpt-6-luna",
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
        specs: DeviceTraitsAndSpecifications | None = None,
    ) -> str:
        """User-facing description built only from the seller description and extracted specs."""
        user_content = name.strip() or "Unknown device"
        if description and description.strip():
            user_content = f"{user_content}\n\nSeller description: {description.strip()}"
        if specs is not None:
            extracted = specs.model_dump(exclude_none=True)
            if extracted:
                user_content = f"{user_content}\n\nExtracted specifications: {json.dumps(extracted, ensure_ascii=False)}"
        if price is not None:
            user_content = f"{user_content}\n\nSeller price: {price} USD"
        response = self.client.chat.completions.create(
            model="gpt-6-luna",
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

    def get_device_specs_by_name(
        self,
        name: str,
        description: str | None = None,
    ) -> DeviceTraitsAndSpecifications:
        """Get device params by name and optional seller description in JSON format: os, category, brand..."""
        if not (name and name.strip()):
            return DeviceTraitsAndSpecifications()

        user_content = name.strip()
        if description and description.strip():
            user_content = f"{user_content}\n\nSeller description: {description.strip()}"

        specifications_prompt: str = GET_TRAITS_BY_DEVICE_NAME_PROMPT.format(
            traits_fields=TRAITS_FIELDS_DEVICE,
            specifications_fields=SPECIFICATIONS_FIELDS_DEVICE,
            key_features_device_fields=KEY_FEATURES_DEVICE_FIELDS
        )

        response = self.client.chat.completions.create(
            model="gpt-6-luna",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": specifications_prompt},
                {"role": "user", "content": user_content},
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
            model="gpt-6-luna",
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

    def rerank_devices(self, user_prompt: str, candidates: list[dict]) -> list[dict]:
        """Keep only candidates that satisfy the request, best match first. Falls back to vector order on LLM errors."""
        if not candidates:
            return []

        payload = {
            "request": user_prompt.strip(),
            "candidates": [
                {
                    "id": index,
                    "name": c.get("name", ""),
                    "price": c.get("price"),
                    "key_features": c.get("key_features", []),
                    "specifications": c.get("specifications", {}),
                    "traits": c.get("traits", {}),
                }
                for index, c in enumerate(candidates)
            ],
        }

        try:
            response = self.client.chat.completions.create(
                model="gpt-6-luna",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": RERANK_DEVICES_PROMPT},
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False, default=str)},
                ],
            )
            content = response.choices[0].message.content if response.choices else ""
            data = dirtyjson.loads(content or "{}") or {}
            ids = data.get("ids", []) if isinstance(data, dict) else []
        except (dirtyjson.Error, OpenAIError, TypeError, ValueError) as error:
            print(f"Rerank failed, using vector order: {error}")
            return candidates

        result: list[dict] = []
        seen: set[int] = set()
        for raw_id in ids:
            try:
                index = int(raw_id)
            except (TypeError, ValueError):
                continue
            if 0 <= index < len(candidates) and index not in seen:
                seen.add(index)
                result.append(candidates[index])
        return result


device_service = DeviceService()
