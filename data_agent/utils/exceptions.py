"""Custom exceptions for the data_agent package."""


class DataAgentError(Exception):
    """Base for all errors in the data_agent package."""

    def __str__(self) -> str:
        # Every subclass inherits this, so every message starts with the prefix.
        return f"[DataAgent] {super().__str__()}"


class ProfilerError(DataAgentError):
    """Raised for profiler-related failures."""


class InvalidColumnError(ProfilerError):
    """Raised when a column fails validation."""

    def __init__(self, message: str, column_name: str, bad_value=None):
        super().__init__(message)          # tells Exception which argument is the message
        self.column_name = column_name
        self.bad_value = bad_value

    def __str__(self) -> str:
        return f"{super().__str__()} | column={self.column_name!r} (got {self.bad_value!r})"


class ProfileNotFoundError(ProfilerError):
    """Raised when a column lookup finds nothing."""

    def __init__(self, message: str, column_name: str):
        super().__init__(message)
        self.column_name = column_name

    def __str__(self) -> str:
        return f"{super().__str__()} | column={self.column_name!r}"


class DataNotLoadedError(DataAgentError):
    """Raised when a question is asked before any data has been loaded."""
    # No __init__ or __str__ needed: the inherited ones already do the job.


class MemoryNotFoundError(DataAgentError):
    """Raised when a memory key has nothing stored under it."""

    def __init__(self, message: str, key: str):
        super().__init__(message)
        self.key = key

    def __str__(self) -> str:
        return f"{super().__str__()} | key={self.key!r}"