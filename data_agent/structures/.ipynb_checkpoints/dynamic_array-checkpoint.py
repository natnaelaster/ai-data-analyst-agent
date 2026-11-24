
class DynamicArray:

    def __init__(self) -> None:
        self._capacity: int = 2
        self._size: int = 0
        self.copies: int = 0
        self._items: list = [None] * self._capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    def __len__(self) -> int:
        return self._size

    def _normalize_index(self, index: int, allow_end: bool = False) -> int:
        """Translates negative indexes and validates bounds."""
        raw_index = index
        if index < 0:
            index += self._size

        upper_bound = self._size + 1 if allow_end else self._size
        if index < 0 or index >= upper_bound:
            raise IndexError(f"Index {raw_index} out of range for size {self._size}")
        return index

    def __getitem__(self, index: int):
        idx = self._normalize_index(index)
        return self._items[idx]

    def __setitem__(self, index: int, value) -> None:
        idx = self._normalize_index(index)
        self._items[idx] = value

    def _resize(self, new_capacity: int) -> None:
        new_items = [None] * new_capacity
        for i in range(self._size):
            new_items[i] = self._items[i]
            self.copies += 1

        self._items = new_items
        self._capacity = new_capacity

    def append(self, value) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        self._items[self._size] = value
        self._size += 1

    def insert(self, index: int, value) -> None:
        # Clamp or normalize index to match Python's list.insert behavior
        if index < 0:
            index = max(0, self._size + index)
        elif index > self._size:
            index = self._size

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        # Shift elements right from the back to make room
        for i in range(self._size, index, -1):
            self._items[i] = self._items[i - 1]

        self._items[index] = value
        self._size += 1

    def pop(self, index: int = -1):
        if self._size == 0:
            raise IndexError(f"Index {index} out of range for size {self._size}")

        idx = self._normalize_index(index)
        removed_value = self._items[idx]

        # Shift elements left to close the gap
        for i in range(idx, self._size - 1):
            self._items[i] = self._items[i + 1]

        # Clear the trailing slot to avoid holding stale object references
        self._items[self._size - 1] = None
        self._size -= 1
        return removed_value

    def __iter__(self):
        for i in range(self._size):
            yield self._items[i]

    def __contains__(self, item) -> bool:
        for i in range(self._size):
            if self._items[i] == item:
                return True
        return False

    def __repr__(self) -> str:
        elements = ", ".join(repr(item) for item in self)
        return f"DynamicArray([{elements}])"
