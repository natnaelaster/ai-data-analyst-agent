from .column import ColumnProfile, CategoricalColumn, NumericColumn

__all__ = [
    "ColumnProfile",
    "CategoricalColumn",
    "NumericColumn",
    "DatasetProfile",
]


def __getattr__(name: str):
    if name == "DatasetProfile":
        from .dataset import DatasetProfile
        return DatasetProfile
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")