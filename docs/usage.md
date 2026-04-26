# API and Client Reference

This page covers the main translation client, the request parameters, and the API behavior.

## API Behavior

- Base URL: `https://tmt.ilprl.ku.edu.np/lang-translate`
- Method: `POST`
- Content type: `application/json`
- Authentication: `Authorization: Bearer <token>`
- Success responses always use HTTP 200.
- The API translates one sentence at a time.
- Translation quality is better when you send clean, logical sentences instead of long paragraphs or mixed clauses.

## `TMTTranslationClient(api_key, base_url=..., timeout=30.0, client=None)`

Creates a client instance.

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `api_key` | Yes | Bearer token for the TMT API. Pass it directly when constructing the client. |
| `base_url` | No | Override for the API endpoint. Defaults to `https://tmt.ilprl.ku.edu.np/lang-translate`. |
| `timeout` | No | HTTP timeout passed to `httpx`. Defaults to `30.0` seconds. |
| `client` | No | Preconfigured `httpx.Client` for testing or advanced transport setup. |

## `translate(text, src_lang, tgt_lang) -> TranslationResponse`

Translates a single sentence.

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `text` | Yes | Sentence to translate. |
| `src_lang` | Yes | Source language. Accepts `English`, `Nepali`, `Tamang` and their supported code forms. |
| `tgt_lang` | Yes | Target language. Must be different from `src_lang`. |

Raises:

- `AuthenticationError` for 401 responses or missing credentials.
- `RequestValidationError` for invalid request payloads or 400 responses.
- `APIError` for API failures or malformed responses.

## `translate_many(texts, src_lang, tgt_lang) -> list[TranslationResponse]`

Translates a list of sentences sequentially.

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `texts` | Yes | Sequence of sentence strings to translate one by one. |
| `src_lang` | Yes | Source language for every sentence in `texts`. |
| `tgt_lang` | Yes | Target language for every sentence in `texts`. |

## `translate_document(text, src_lang, tgt_lang) -> str`

Splits the text into sentences, translates each sentence, and joins the translated sentences back together.

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `text` | Yes | Full document text to split and translate sentence by sentence. |
| `src_lang` | Yes | Source language for the document. |
| `tgt_lang` | Yes | Target language for the document. |

## Response Model

`TranslationResponse` exposes the API fields as attributes:

- `message_type`
- `message`
- `src_lang`
- `input`
- `target_lang`
- `output`
- `timestamp`

Use `response.success` to check whether the API reported success.

## Error Reference

The SDK maps the documented API failures to Python exceptions:

- `401` missing or malformed auth header -> `AuthenticationError`
- `401` invalid token -> `AuthenticationError`
- `400` invalid JSON/body -> `RequestValidationError`
- `400` missing `text`, `src_lang`, or `tgt_lang` -> `RequestValidationError`
- `400` same source and target language -> `RequestValidationError`
- `500` translation failure -> `APIError`
