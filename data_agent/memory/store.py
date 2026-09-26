class MemoryStore:
    """Placeholder for the memory store.

    Will hold conversation history, embeddings, or retrieved context
    as the agent grows. Currently empty on purpose.
    """
    pass

class MemoryStore:
    def __repr__(self):
        return "MemoryStore(empty — placeholder)"

class BaseTool:
    def __repr__(self):
        return "BaseTool(empty — placeholder)"

if __name__ == "__main__":
    store = MemoryStore()
    print(store)