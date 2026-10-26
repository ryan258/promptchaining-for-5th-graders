"""Safe errors shared by local execution surfaces. Never echo provider payloads."""

from openai import AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError, BadRequestError


class InputError(ValueError):
    """Only application-authored, safe-to-display validation messages belong here."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def user_error(exc: Exception) -> str:
    if isinstance(exc, InputError):
        return str(exc)
    if isinstance(exc, AuthenticationError):
        return "The provider did not accept the key. Check .env privately, then restart."
    if isinstance(exc, RateLimitError):
        return "The provider reported a usage or rate limit. Check your account before trying again."
    if isinstance(exc, APITimeoutError):
        return "The request timed out and may have been processed. Check provider usage before trying again."
    if isinstance(exc, APIConnectionError):
        return "Could not reach the provider. Check your connection before trying again."
    if isinstance(exc, BadRequestError):
        return "The provider rejected the request. Check the model, context size and configured limits."
    return "The operation could not finish. Check local setup, model configuration and provider usage before trying again."
