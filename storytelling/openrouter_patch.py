import os
from typing import Any, ClassVar, Dict, List, Optional

import requests
from langchain_core.language_models.llms import LLM
from pydantic import Field


class PatchedOpenRouterLLM(LLM):
    """A patched version of the OpenRouterLLM class that is compatible with Pydantic V2."""

    URL: ClassVar[str] = "https://openrouter.ai/api/v1/chat/completions"

    model_name: str = Field(..., alias="model_name")
    temperature: float = 0.7

    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": self.temperature,
        }
        if stop:
            data["stop"] = stop

        response = requests.post(self.URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["text"]

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {"model_name": self.model_name, "temperature": self.temperature}
