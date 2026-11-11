import pandas as pd
import csv
import time
from data_agent.utils import is_valid_column_name
from data_agent.utils import timed, retry
from data_agent.utils import iter_rows, batched
from data_agent.utils import DataAgentError, ProfilerError, InvalidColumnError, ProfileNotFoundError
from data_agent.profiler import ColumnProfile, DatasetProfile

if __name__ == "__main__":
    # Test cases for the data_agent package
    # Test 1 — DataAgentError
    try:
        raise DataAgentError("base agent failure")
    except DataAgentError as e:
        print(f"Test 1 (DataAgentError): {e}")
        # Verify the [DataAgent] prefix
        assert str(e).startswith("[DataAgent]"), "prefix missing"

    # Test 2 — ProfilerError
    try:
        raise ProfilerError("profiler failure")
    except ProfilerError as e:
        print(f"Test 2 (ProfilerError): {e}")
        # Verify inheritance: ProfilerError should also print [DataAgent]
        assert str(e).startswith("[DataAgent]"), "prefix missing"

    # Test 3 — InvalidColumnError via ColumnProfile
    try:
        ColumnProfile("hulu", "int64", -90, 100)
    except InvalidColumnError as e:
        assert e.column_name == "hulu"
        assert e.bad_value == -90
        assert str(e).startswith("[DataAgent]")
    else:
        raise AssertionError("InvalidColumnError was not raised")


    # Test 4 — ProfileNotFoundError via DatasetProfile
    profile = DatasetProfile()
    
    try:
        profile["missing_column"]
    except ProfileNotFoundError as e:
        assert e.column_name == "missing_column"
    else:
        raise AssertionError("ProfileNotFoundError was not raised")    
    
    # Test 5 — timed and retry decorators
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
        
    # Example usage of iter_rows
    for row in iter_rows("output.csv"):
        print(row)
    
    # Example usage of batched
    data = range(7)
    for batch in batched(data, 3):
        print(batch)
    
    #import pandas as pd
    df = pd.DataFrame({'revenue': [100, 200, None], 'country': ['ET', 'US', 'ET']})
    profile = DatasetProfile.from_dataframe(df)
    profile.quality_report()  
    print(f"Null rates: {profile.null_rates}")                                   
    print(f"Dirty columns: {profile.dirty_columns}")
    '''
    
    # timed: result passes through AND @wraps kept the name (the two classic bugs)
    @timed
    def quick():
        return "done"
    assert quick() == "done"
    assert quick.__name__ == "quick"

    # retry: fails twice, then succeeds
    calls = {"n": 0}                   # a dict, so the inner function can change it without `nonlocal`

    @retry(times=3)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("simulated drop")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3

    # retry: always fails, so the last error must propagate
    @retry(times=2)
    def always_fails():
        raise ConnectionError("down")

    try:
        always_fails()
    except ConnectionError:
        pass
    else:
        raise AssertionError("ConnectionError was not raised")

    # batched
    assert list(batched(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]
    assert list(batched([], 3)) == []

    # iter_rows: write a temp file, read it back, always clean up
    from pathlib import Path
    tmp = Path("_tmp_rows.csv")
    try:
        with open(tmp, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "score"])
            writer.writeheader()
            writer.writerows([{"name": "a", "score": 1}, {"name": "b", "score": 2}])
        assert list(iter_rows(tmp)) == [
            {"name": "a", "score": "1"},    # csv always reads values back as strings
            {"name": "b", "score": "2"},
        ]
    finally:
        tmp.unlink()                        # runs even if the assert above fails'''