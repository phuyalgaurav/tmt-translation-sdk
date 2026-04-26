"""Response models for the TMT Translation API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class TranslationResponse:
    message_type: str
    message: str
    src_lang: str
    input: str
    target_lang: str
    output: str
    timestamp: str

    @property
    def success(self) -> bool:
        return self.message_type.upper() == "SUCCESS"

    @classmethod
    def from_json(cls, payload: Mapping[str, Any]) -> "TranslationResponse":
        required_fields = (
            "message_type",
            "message",
            "src_lang",
            "input",
            "target_lang",
            "output",
            "timestamp",
        )
        missing = [field for field in required_fields if field not in payload]
        if missing:
            raise ValueError(
                f"Response payload is missing required fields: {', '.join(missing)}"
            )

        return cls(
            message_type=str(payload["message_type"]),
            message=str(payload["message"]),
            src_lang=str(payload["src_lang"]),
            input=str(payload["input"]),
            target_lang=str(payload["target_lang"]),
            output=str(payload["output"]),
            timestamp=str(payload["timestamp"]),
        )
