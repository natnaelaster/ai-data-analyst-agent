class MemoryStore:
    """Dict-backed memory. Replaced by a hash-table version in Week 2."""

    def __init__(self): ...
    def store(self, key: str, value) -> None: ...
    def retrieve(self, key: str): ...       # raises MemoryNotFoundError if missing
    def __len__(self) -> int: ...
    def __contains__(self, key: str) -> bool: ...
    def __repr__(self) -> str: ...

class BaseTool:
    def __repr__(self):
        return "BaseTool(empty — placeholder)"

if __name__ == "__main__":
    store = MemoryStore()
    print(store)