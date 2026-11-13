import time
from functools import wraps

def timed (func):
    """Decorator to measure the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def retry(times):
    if times < 1:
        raise ValueError("times must be >= 1, got {times}")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    last_error = e
                    print(f"Attempt {attempt}/{times} failed: {e}")
            raise last_error
        return wrapper
    return decorator

