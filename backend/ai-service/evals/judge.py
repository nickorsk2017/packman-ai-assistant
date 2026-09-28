"""LLM judge shared by all DeepEval metrics."""

from functools import lru_cache

from deepeval.models import OpenAIModel

from app.config import settings


@lru_cache(maxsize=1)
def judge_model() -> OpenAIModel:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set")
    return OpenAIModel(model=settings.eval_judge_model, api_key=settings.openai_api_key)
