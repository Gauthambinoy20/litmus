from typing import Any


class LitmusError(Exception):
    message: str = "An unexpected error occurred"
    error_code: str = "INTERNAL_ERROR"
    status_code: int = 500

    def __init__(self, message: str | None = None, details: dict[str, Any] | None = None) -> None:
        self.message = message or self.__class__.message
        self.details = details or {}
        super().__init__(self.message)


class ResumeEmptyError(LitmusError):
    message = "Resume text is empty"
    error_code = "RESUME_EMPTY"
    status_code = 400


class JDEmptyError(LitmusError):
    message = "Job description text is empty"
    error_code = "JD_EMPTY"
    status_code = 400


class InputTooShortError(LitmusError):
    message = "Input text is below minimum length"
    error_code = "INPUT_TOO_SHORT"
    status_code = 400


class InputTooLongError(LitmusError):
    message = "Input text exceeds maximum length"
    error_code = "INPUT_TOO_LONG"
    status_code = 400


class InvalidFileError(LitmusError):
    message = "Uploaded file is not a valid PDF or DOCX"
    error_code = "INVALID_FILE"
    status_code = 400


class EncryptedPDFError(LitmusError):
    message = "PDF is password-protected and cannot be read"
    error_code = "ENCRYPTED_PDF"
    status_code = 400


class FileTooLargeError(LitmusError):
    message = "File exceeds the 10MB size limit"
    error_code = "FILE_TOO_LARGE"
    status_code = 413


class EmptyDocumentError(LitmusError):
    message = "Document has no extractable text"
    error_code = "EMPTY_DOCUMENT"
    status_code = 400


class RateLimitExceededError(LitmusError):
    message = "Rate limit exceeded. Please try again later."
    error_code = "RATE_LIMIT_EXCEEDED"
    status_code = 429


class EngineError(LitmusError):
    message = "Internal engine failure"
    error_code = "ENGINE_ERROR"
    status_code = 500
