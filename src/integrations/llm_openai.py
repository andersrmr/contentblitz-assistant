import json

from openai import OpenAI

from app.config import settings


class LLMError(RuntimeError):
    pass


class OpenAIClient:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key if api_key is not None else settings.OPENAI_API_KEY
        self.model = model if model is not None else settings.OPENAI_MODEL
        self._client = OpenAI(api_key=self.api_key) if self.api_key else None

    def _create_response(self, system: str, user: str, temperature: float):
        if self._client is None:
            raise LLMError("OpenAI API key is not configured.")
        try:
            return self._client.responses.create(
                model=self.model,
                temperature=temperature,
                input=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
        except Exception as exc:  # pragma: no cover - exercised via integration only
            raise LLMError(f"OpenAI request failed: {exc}") from exc

    def _extract_text(self, response: object) -> str:
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str) and output_text.strip():
            return output_text

        output = getattr(response, "output", None) or []
        text_chunks: list[str] = []
        for item in output:
            content = getattr(item, "content", None) or []
            for part in content:
                text = getattr(part, "text", None)
                if isinstance(text, str) and text.strip():
                    text_chunks.append(text)
        if text_chunks:
            return "".join(text_chunks)
        raise LLMError("OpenAI response did not contain text.")

    def _request_text(self, system: str, user: str, temperature: float) -> str:
        response = self._create_response(system=system, user=user, temperature=temperature)
        return self._extract_text(response)

    @staticmethod
    def _strip_json_fences(text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()
        return cleaned

    def complete_text(self, system: str, user: str, temperature: float = 0.2) -> str:
        return self._request_text(system=system, user=user, temperature=temperature)

    def complete_json(
        self,
        system: str,
        user: str,
        temperature: float = 0.0,
        max_retries: int = 1,
    ) -> dict:
        json_system = (
            f"{system}\n\n"
            "Return JSON only. Do not use markdown. Do not wrap the response in code fences."
        )
        current_user = user
        attempts = max_retries + 1
        last_error: Exception | None = None

        for _ in range(attempts):
            raw_text = self._request_text(system=json_system, user=current_user, temperature=temperature)
            cleaned = self._strip_json_fences(raw_text)
            try:
                parsed = json.loads(cleaned)
            except json.JSONDecodeError as exc:
                last_error = exc
                current_user = (
                    "Your previous response was not valid JSON. "
                    "Repair it and return only strict JSON with no markdown.\n\n"
                    f"Previous response:\n{cleaned}"
                )
                continue
            if not isinstance(parsed, dict):
                raise LLMError("OpenAI JSON response was not an object.")
            return parsed

        raise LLMError(f"Failed to parse JSON response: {last_error}")
