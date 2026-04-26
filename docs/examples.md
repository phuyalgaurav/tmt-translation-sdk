# Examples

This page contains copy-paste-ready examples for common SDK workflows.

## 1. Basic sentence translation

```python
from tmt_translation_sdk import TMTTranslationClient

client = TMTTranslationClient(api_key="team_xxxxxxxxxxxxxxxx")
response = client.translate("Hello, how are you?", "en", "ne")

if response.success:
    print(response.output)
else:
    print(response.message)
```

## 2. Translate multiple sentences

```python
from tmt_translation_sdk import TMTTranslationClient

sentences = [
    "Hello everyone.",
    "Welcome to the workshop.",
    "We will begin in five minutes.",
]

client = TMTTranslationClient(api_key="team_xxxxxxxxxxxxxxxx")
results = client.translate_many(sentences, "en", "ne")

for result in results:
    print(result.output)
```

## 3. Translate a full document

```python
from tmt_translation_sdk import TMTTranslationClient

text = """
Today we will discuss the project timeline. The first milestone is due next week.
Please review your assigned tasks and send updates by Friday.
"""

client = TMTTranslationClient(api_key="team_xxxxxxxxxxxxxxxx")
translated = client.translate_document(text, "en", "ne")
print(translated)
```

## 4. Normalize rough input before translation

```python
from tmt_translation_sdk import TMTTranslationClient, logical_sentence_chunks

rough_text = "i went to the market and bought vegetables but it started raining so i came home"
chunks = logical_sentence_chunks(rough_text)

client = TMTTranslationClient(api_key="team_xxxxxxxxxxxxxxxx")
results = client.translate_many(chunks, "en", "ne")

for result in results:
    print(result.output)
```

## 5. Handle API errors cleanly

```python
from tmt_translation_sdk import (
    APIError,
    AuthenticationError,
    RequestValidationError,
    TMTTranslationClient,
)

try:
    client = TMTTranslationClient(api_key="team_xxxxxxxxxxxxxxxx")
    response = client.translate("Hello", "en", "ne")
    print(response.output)
except AuthenticationError as exc:
    print("Authentication failed:", exc)
except RequestValidationError as exc:
    print("Bad request:", exc)
except APIError as exc:
    print("API error:", exc)
```

## 6. Use with context manager

```python
from tmt_translation_sdk import TMTTranslationClient

with TMTTranslationClient(api_key="team_xxxxxxxxxxxxxxxx") as client:
    result = client.translate("How are you?", "en", "ne")
    print(result.output)
```

## 7. cURL request (API-level)

```bash
curl -X POST https://tmt.ilprl.ku.edu.np/lang-translate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer team_xxxxxxxxxxxxxxxx" \
  -d '{
    "text": "Hello, how are you?",
    "src_lang": "en",
    "tgt_lang": "ne"
  }'
```

## 8. Supported language code examples

```python
from tmt_translation_sdk import TMTTranslationClient

client = TMTTranslationClient(api_key="team_xxxxxxxxxxxxxxxx")

# English -> Nepali
print(client.translate("Hello", "en", "ne").output)

# Nepali -> Tamang
print(client.translate("नमस्ते", "Nepali", "tmg").output)

# Tamang -> English
print(client.translate("...", "tamang", "eng").output)
```
