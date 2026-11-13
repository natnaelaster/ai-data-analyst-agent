"""The DataAgent: loads a CSV, remembers things, and answers questions about it."""

from pathlib import Path

import pandas as pd

from .profiler import DatasetProfile
from .utils import DataNotLoadedError, timed


class DataAgent:
    """Answers questions about a loaded CSV dataset.

    Memory is passed in, not created here. Any object with
    store(key, value) and retrieve(key) methods works.
    """

    def __init__(self, name: str, memory) -> None:
        # __init__ must return None, so it only sets attributes. No return value.
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"name must be a non-empty string, got {name!r}")
        self.name = name
        self.memory = memory                                  # received, not created
        self.profile: DatasetProfile | None = None            # set by load_data()
        self._history: list[tuple[str, str]] = []             # (query, answer) pairs

    @timed
    def load_data(self, filepath: Path) -> None:
        """Read a CSV, build its profile, and remember which file was loaded."""
        path = Path(filepath)                                 # accept str or Path
        if path.suffix.lower() != ".csv":
            raise ValueError(f"expected a .csv file, got {path.suffix!r}")
        if not path.exists():
            raise FileNotFoundError(f"no such file: {path}")

        df = pd.read_csv(path)
        if df.empty:                                          # header only, no rows
            raise ValueError(f"{path.name} has no data rows")

        self.profile = DatasetProfile.from_dataframe(df)
        self.remember("last_file", str(filepath))

    def remember(self, key: str, value) -> None:
        self.memory.store(key, value)                         # delegate, don't duplicate

    def recall(self, key: str):
        return self.memory.retrieve(key)

    def respond(self, query: str) -> str:
        """Answer a question by keyword. Becomes an LLM call in Week 6."""
        if not isinstance(query, str) or not query.strip():
            raise ValueError(f"query must be a non-empty string, got {query!r}")
        if self.profile is None:
            raise DataNotLoadedError("load data before asking questions")

        q = query.lower()
        if "column" in q:
            answer = "Columns: " + ", ".join(col.name for col in self.profile)
        elif "null" in q or "missing" in q:
            dirty = self.profile.dirty_columns
            if dirty:
                rates = self.profile.null_rates
                answer = "Columns with missing values: " + ", ".join(
                    f"{name} ({rates[name]:.1%})" for name in dirty
                )
            else:
                answer = "No column is above the 5% missing-value threshold."
        elif "summary" in q:
            answer = "\n".join(col.summary() for col in self.profile)
        else:
            answer = "I can answer questions about: columns, null/missing values, summary."

        self._history.append((query, answer))
        return answer

    @property
    def history(self) -> list[tuple[str, str]]:
        return list(self._history)        # a copy: callers can't change the internal list

    def __repr__(self) -> str:
        try:
            items = len(self.memory)
        except TypeError:                 # a passed-in memory may not define __len__
            items = "?"
        return (f"DataAgent(name={self.name!r}, "
                f"data_loaded={self.profile is not None}, memory_items={items})")