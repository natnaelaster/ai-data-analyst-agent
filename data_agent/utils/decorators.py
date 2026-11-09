import time
from functools import wraps

def timed (func):
    """Decorator to measure the execution time of a function."""
    wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter() - start_time
        print(f"{func.__name__} took {end_time:.4f}s")
        return result
    return wrapper

def retry(times):
    def decorator(func):
        wraps(func)
        def wrapper(*args, **kwargs):
            last_error = 0
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    last_error = e
                    print(f"Attempt {attempt}/{times} failed: {e}")
            raise last_error
        return wrapper
    return decorator

if __name__ == "__main__":
    @timed
    def test_function():
        time.sleep(1)
        return "Function completed"
    
    @retry(times=3)
    def unreliable_function():
        raise ConnectionError("Simulated connection error")

    # Test the timed decorator
    result = test_function()
    print(result)

    # Test the retry decorator
    try:
        unreliable_function()
    except ConnectionError as e:
        print(f"Final error: {e}")