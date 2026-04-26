# Fast Sentence Normalizer

Use this helper when your input is a rough paragraph, a draft, or a sentence that is too long and awkward to translate directly.

The normalizer is intentionally lightweight and fast. It does not use a heavy NLP model. Instead, it applies simple heuristics to:

- collapse messy whitespace,
- split on sentence-ending punctuation,
- break very long clauses into smaller chunks when needed,
- keep output readable for sentence-by-sentence translation.

## `logical_sentence_chunks(text, max_words=24) -> list[str]`

Returns cleaned sentence-like chunks.

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `text` | Yes | Raw text that may be long, unpunctuated, or contain mixed clauses. |
| `max_words` | No | Upper limit used to split overly long chunks. Defaults to `24`. |

Example:

```python
from tmt_translation_sdk import logical_sentence_chunks

rough_text = "i went to the market and bought vegetables but it started raining so i came home"
print(logical_sentence_chunks(rough_text))
```

## `logical_sentence_text(text, max_words=24) -> str`

Returns the cleaned chunks joined into one readable string.

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `text` | Yes | Raw text to normalize. |
| `max_words` | No | Upper limit used to split overly long chunks. Defaults to `24`. |

Example:

```python
from tmt_translation_sdk import logical_sentence_text

rough_text = "i went to the market and bought vegetables but it started raining so i came home"
clean_text = logical_sentence_text(rough_text)
print(clean_text)
```

## When to use it

Use the normalizer before calling the translation client when:

- text is one long paragraph,
- sentence boundaries are missing or messy,
- clauses are crammed together,
- you want a quick cleanup step before translation.

## When not to use it

Do not expect it to rewrite meaning or perform grammar correction. It is a fast heuristic splitter, not a language model.
