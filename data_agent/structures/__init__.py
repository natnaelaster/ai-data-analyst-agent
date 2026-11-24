__all__ = ['DynamicArray']


def __getattr__(name: str):
    if name == "DynamicArray":
        from .dynamic_array import DynamicArray
        return DynamicArray
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")