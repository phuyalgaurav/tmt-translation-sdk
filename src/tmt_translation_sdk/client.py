"""Client for the TMT Translation API."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import httpx

from .exceptions import APIError, AuthenticationError, RequestValidationError
from .models import TranslationResponse
from .text import logical_sentence_chunks

_BASE_URL = "https://tmt.ilprl.ku.edu.np/lang-translate"
_LANGUAGE_ALIASES = {
    "en": "English",
    "eng": "English",
    "english": "English",
    "ne": "Nepali",
    "nep": "Nepali",
    "nepali": "Nepali",
    "tmg": "Tamang",
    "tamang": "Tamang",
}


@dataclass(slots=True)
class _RequestPayload:
    text: str
    src_lang: str
    tgt_lang: str

    def to_dict(self) -> dict[str, str]:
        return {
            "text": self.text,
            "src_lang": self.src_lang,
            "tgt_lang": self.tgt_lang,
        }


class TMTTranslationClient:
    """Minimal SDK wrapper around the TMT Translation API."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _BASE_URL,
        timeout: float | httpx.Timeout = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key.strip()
        if not self.api_key:
            raise AuthenticationError(
                "An API key is required. Pass api_key=... when creating TMTTranslationClient."
            )

        self.base_url = base_url.rstrip("/")
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=timeout)
        self._default_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "TMTTranslationClient":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def translate(self, text: str, src_lang: str, tgt_lang: str) -> TranslationResponse:
        """Translate a single sentence using the TMT API."""

        payload = self._validate_payload(text, src_lang, tgt_lang)
        response = self._client.post(
            self.base_url,
            json=payload.to_dict(),
            headers=self._default_headers,
        )
        return self._parse_response(response)

    def translate_many(
        self,
        texts: Sequence[str],
        src_lang: str,
        tgt_lang: str,
    ) -> list[TranslationResponse]:
        """Translate multiple independent sentences one request at a time."""

        return [self.translate(text, src_lang, tgt_lang) for text in texts]

    def translate_document(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Split a document into sentences, translate each one, and reassemble the result."""

        sentences = logical_sentence_chunks(text)
        if not sentences:
            return ""

        translated = [
            self.translate(sentence, src_lang, tgt_lang).output
            for sentence in sentences
        ]
        return " ".join(translated)

    @staticmethod
    def normalize_language(language: str) -> str:
        key = language.strip().lower()
        if key not in _LANGUAGE_ALIASES:
            raise RequestValidationError(
                f"Unsupported language: {language}. Supported values are English, Nepali, and Tamang."
            )
        return _LANGUAGE_ALIASES[key]

    def _validate_payload(
        self, text: str, src_lang: str, tgt_lang: str
    ) -> _RequestPayload:
        if not text or not text.strip():
            raise RequestValidationError("text is required and cannot be empty.")

        normalized_src = self.normalize_language(src_lang)
        normalized_tgt = self.normalize_language(tgt_lang)
        if normalized_src == normalized_tgt:
            raise RequestValidationError("src_lang and tgt_lang must be different.")

        return _RequestPayload(
            text=text, src_lang=normalized_src, tgt_lang=normalized_tgt
        )

    def _parse_response(self, response: httpx.Response) -> TranslationResponse:
        try:
            payload: Any = response.json()
        except ValueError as exc:
            raise APIError(
                "The API returned a non-JSON response.", response=response
            ) from exc

        if response.status_code == 401:
            raise AuthenticationError(
                self._extract_error_message(payload), response=response
            )
        if response.status_code == 400:
            raise RequestValidationError(
                self._extract_error_message(payload), response=response
            )
        if response.status_code >= 500:
            raise APIError(self._extract_error_message(payload), response=response)

        if not isinstance(payload, dict):
            raise APIError(
                "The API returned an unexpected payload shape.", response=response
            )

        translation = TranslationResponse.from_json(payload)
        if translation.success:
            return translation

        raise APIError(translation.message or "Translation failed.", response=response)

    @staticmethod
    def _extract_error_message(payload: Any) -> str:
        if isinstance(payload, dict):
            message = payload.get("message")
            if message:
                return str(message)
        return "The API request failed."
