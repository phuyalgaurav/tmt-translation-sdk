"""Fast text normalization helpers for sentence-level translation."""

from __future__ import annotations

import re
from collections.abc import Iterable

_SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?।])\s+")
_CLAUSE_SPLIT_RE = re.compile(
    r"\s+(?=(?:and|but|so|because|then|however|therefore|also|moreover)\b)",
    re.IGNORECASE,
)
_WHITESPACE_RE = re.compile(r"\s+")


def logical_sentence_chunks(text: str, *, max_words: int = 24) -> list[str]:
    """Return fast, sentence-like chunks from rough input text.

    This is a heuristic normalizer. It does not rewrite meaning, but it can
    quickly turn messy text into cleaner chunks that translate better than one
    long paragraph.
    """

    cleaned = _normalize_whitespace(text)
    if not cleaned:
        return []

    chunks: list[str] = []
    for sentence in _split_on_boundaries(cleaned):
        chunks.extend(_split_long_clause(sentence, max_words=max_words))
    return [chunk for chunk in (item.strip() for item in chunks) if chunk]


def logical_sentence_text(text: str, *, max_words: int = 24) -> str:
    """Return rough text normalized into a readable sentence string."""

    return " ".join(logical_sentence_chunks(text, max_words=max_words))


def _split_on_boundaries(text: str) -> list[str]:
    parts = _SENTENCE_BOUNDARY_RE.split(text)
    if len(parts) == 1:
        return [text]
    return [part.strip() for part in parts if part.strip()]


def _split_long_clause(sentence: str, *, max_words: int) -> list[str]:
    words = sentence.split()
    if len(words) <= max_words:
        return [sentence]

    clause_parts = _CLAUSE_SPLIT_RE.split(sentence)
    if len(clause_parts) == 1:
        return _split_by_length(words, max_words=max_words)

    chunks: list[str] = []
    current: list[str] = []
    for part in clause_parts:
        part_words = part.split()
        if not part_words:
            continue
        if len(current) + len(part_words) > max_words and current:
            chunks.append(" ".join(current))
            current = []
        current.extend(part_words)
    if current:
        chunks.append(" ".join(current))
    return chunks or [sentence]


def _split_by_length(words: list[str], *, max_words: int) -> list[str]:
    return [
        " ".join(words[index : index + max_words])
        for index in range(0, len(words), max_words)
    ]


def _normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()
