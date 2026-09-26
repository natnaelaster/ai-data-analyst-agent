def is_valid_column_name(name: str) -> bool:
    """Return True if `name` is a non-empty string."""
    return isinstance(name, str) and len(name.strip()) > 0


def is_positive_int(value) -> bool:
    """Return True if `value` is a positive integer."""
    return isinstance(value, int) and value > 0

def validate_null_count(null_count: int, total_count: int) -> None:
    """Raise ValueError if null_count is invalid relative to total_count."""
    if null_count < 0:
        raise ValueError(f"null_count must be >= 0, got {null_count}")
    if null_count > total_count:
        raise ValueError(
            f"null_count ({null_count}) cannot exceed total_count ({total_count})"
        )

if __name__ == "__main__":
    print(is_valid_column_name("country"))   # True
    print(is_valid_column_name(""))          # False
    print(is_positive_int(5))                # True
    print(is_positive_int(-1))               # False