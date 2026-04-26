from __future__ import annotations

import json

import httpx
import pytest

from tmt_translation_sdk import (
    APIError,
    AuthenticationError,
    RequestValidationError,
    TMTTranslationClient,
)
from tmt_translation_sdk.text import logical_sentence_chunks, logical_sentence_text


@pytest.fixture()
def translation_payload() -> dict[str, str]:
    return {
        "message_type": "SUCCESS",
        "message": "Translated successfully.",
        "src_lang": "English",
        "input": "Hello",
        "target_lang": "Nepali",
        "output": "नमस्ते",
        "timestamp": "2026-04-26T00:00:00Z",
    }


def test_translate_success(translation_payload: dict[str, str]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer test-key"
        assert request.url == httpx.URL("https://tmt.ilprl.ku.edu.np/lang-translate")
        return httpx.Response(200, json=translation_payload)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    sdk = TMTTranslationClient(api_key="test-key", client=client)

    result = sdk.translate("Hello", "en", "ne")

    assert result.success is True
    assert result.output == "नमस्ते"
    assert result.target_lang == "Nepali"


@pytest.mark.parametrize("src_lang,tgt_lang", [("en", "en"), ("Nepali", "ne")])
def test_translate_rejects_same_language(src_lang: str, tgt_lang: str) -> None:
    sdk = TMTTranslationClient(api_key="test-key", client=httpx.Client())

    with pytest.raises(RequestValidationError, match="must be different"):
        sdk.translate("Hello", src_lang, tgt_lang)


def test_missing_api_key_raises() -> None:
    with pytest.raises(TypeError):
        TMTTranslationClient(client=httpx.Client())


def test_translate_raises_on_fail_response() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "message_type": "FAIL",
                "message": "Translation failed",
                "src_lang": "English",
                "input": "Hello",
                "target_lang": "Nepali",
                "output": "",
                "timestamp": "2026-04-26T00:00:00Z",
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    sdk = TMTTranslationClient(api_key="test-key", client=client)

    with pytest.raises(APIError, match="Translation failed"):
        sdk.translate("Hello", "en", "ne")


def test_translate_document_splits_sentences() -> None:
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        calls.append(payload["text"])
        return httpx.Response(
            200,
            json={
                "message_type": "SUCCESS",
                "message": "Translated successfully.",
                "src_lang": "English",
                "input": payload["text"],
                "target_lang": "Nepali",
                "output": f"{payload['text']} translated",
                "timestamp": "2026-04-26T00:00:00Z",
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    sdk = TMTTranslationClient(api_key="test-key", client=client)

    result = sdk.translate_document("Hello world. How are you?", "en", "ne")

    assert calls == ["Hello world.", "How are you?"]
    assert result == "Hello world. translated How are you? translated"


def test_logical_sentence_chunks_splits_rough_text() -> None:
    rough_text = "i went to the market and bought vegetables but it started raining so i came home"

    chunks = logical_sentence_chunks(rough_text, max_words=5)

    assert chunks == [
        "i went to the market",
        "and bought vegetables",
        "but it started raining",
        "so i came home",
    ]


def test_logical_sentence_text_normalizes_whitespace() -> None:
    rough_text = "Hello   there\n\nthis is   messy"

    assert logical_sentence_text(rough_text) == "Hello there this is messy"


def test_auth_error_maps_to_authentication_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "Invalid API token"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    sdk = TMTTranslationClient(api_key="bad", client=client)

    with pytest.raises(AuthenticationError, match="Invalid API token"):
        sdk.translate("Hello", "en", "ne")
