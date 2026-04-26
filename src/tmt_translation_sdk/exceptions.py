"""Exceptions raised by the TMT Translation SDK."""

from __future__ import annotations


class TranslationError(Exception):
    """Base exception for SDK errors."""


class APIError(TranslationError):
    """Raised when the API reports a failure or returns an unexpected response."""

    def __init__(self, message: str, *, response: object | None = None) -> None:
        super().__init__(message)
        self.response = response


class AuthenticationError(APIError):
    """Raised when authentication fails."""


class RequestValidationError(APIError):
    """Raised when the request is malformed before it reaches the API."""
