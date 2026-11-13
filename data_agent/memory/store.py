"""Dict-backed memory for the agent. Replaced by a hash-table version in Week 2."""

from ..utils import MemoryNotFoundError   # ".." = one level up, then into utils


class MemoryStore:
    """Key-value memory with the same method names the Week 2 AgentMemory will use."""

    def __init__(self) -> None:
        self._data: dict[str, object] = {}     # underscore = internal, callers use the methods

    def store(self, key: str, value) -> None:
        """Save value under key, replacing anything already there."""
        self._data[key] = value

    def retrieve(self, key: str):
        """Return the value for key, or raise MemoryNotFoundError."""
        if key not in self._data:
            raise MemoryNotFoundError(f"No memory stored under {key!r}", key)
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return f"MemoryStore({len(self)} items)"


if __name__ == "__main__":
    # Run from the project root with:  python -m data_agent.memory.store
    memory = MemoryStore()
    memory.store("last_file", "sales.csv")
    assert memory.retrieve("last_file") == "sales.csv"
    assert "last_file" in memory and len(memory) == 1
    try:
        memory.retrieve("nope")
    except MemoryNotFoundError:
        pass
    else:
        raise AssertionError("MemoryNotFoundError was not raised")
    print(memory)