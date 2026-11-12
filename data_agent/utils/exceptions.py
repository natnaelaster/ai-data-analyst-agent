
class DataAgentError(Exception):
    """Base for all errors in the data_agent package."""
    def __str__(self):
        Base = super().__str__()
        return f"[DataAgent] {Base}"
    
class ProfilerError(DataAgentError):
    """Raised for profiler-related failures."""

class InvalidColumnError(ProfilerError):
    """Raised when a column fails validation."""
    def __init__ (self, message: str, column_name: str, bad_value=None):
        super().__init__(message)
        self.column_name = column_name
        self.bad_value = bad_value
        
    def __str__(self):
        Base = super().__str__()
        return f"{Base} | column={self.column_name!r} (got {self.bad_value!r})"
    
class ProfileNotFoundError(ProfilerError):
    def __init__ (self, message: str, column_name: str):
        super().__init__(message)
        self.column_name = column_name
                
    def __str__(self):
        Base = super().__str__()
        return f"{Base} | column={self.column_name!r}"
    
class DataNotLoadedError(DataAgentError):
    """Raised when data is not loaded before profiling."""
    def __init__(self, message:str):
        super().__init__(message)
        
    def __str__(self):
        Base = super().__str__()
        return f"{Base} | data not loaded"
    
class MemoryNotFoundError(DataAgentError):
    """Raised when memory is not found"""
    def __init__(self, message:str, key:str):
        super().__init__(message)
        self.key = key

    def __str__(self):
        Base = super().__str__()
        return f"{Base} | key={self.key!r}"