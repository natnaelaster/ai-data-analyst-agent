
class DataAgentError(Exception):
    """Base for all errors in the data_agent package."""
    def __str__(self):
        Base = super().__str__()
        return f"[DataAgent] {Base}"
    
class ProfilerError(DataAgentError):
    pass

class InvalidColumnError(ProfilerError):
    def __init__ (self, message: str, column_name: str, bad_value: None):
        super().__init__(message)
        self.column_name = column_name
        self.bad_value = bad_value
        
    def __str__(self):
        Base = super().__str__()
        return f"{base} | column={self.column_name!r} (got {self.bad_value!r})"
    
class ProfileNotFoundError(ProfilerError):
    def __init__ (self, message: str, column_name: str):
        super().__init__(message)
        self.column_name = column_name
                
    def __str__(self):
        Base = super().__str__()
        return f"Column: {self.column_name} {Base}"
    