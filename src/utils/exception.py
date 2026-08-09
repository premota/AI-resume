class AgentInitializationError(Exception):
    """Raised when a PydanticAI agent fails to construct from its config."""


class AgentExecutionError(Exception):
    """Raised when a PydanticAI agent fails during prompt execution."""


class ToolRegistryError(Exception):
    """Raised when one or more tools fail to register onto an agent."""


class TextExtractionError(Exception):
    """Raised when text extraction from a document fails."""


class AppException(Exception):
    status_code = 400
    message = "App Error"
    

class EmailAlreadyExistError(AppException):
    """Raised when registeration is attempted with an email already on file"""
    status_code = 409
    message = "Email already exists"