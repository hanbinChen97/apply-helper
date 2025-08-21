class ApplicationError(Exception):
    """Base class for all application-specific errors."""
    pass

class LLMError(ApplicationError):
    """Raised for errors related to the LLM client."""
    pass

class PDFGenerationError(ApplicationError):
    """Raised for errors during PDF generation."""
    pass

class InvalidJSONResponseError(LLMError):
    """Raised when the LLM returns a response that is not valid JSON."""
    def __init__(self, message="LLM response is not valid JSON.", response_text=None):
        super().__init__(message)
        self.response_text = response_text
