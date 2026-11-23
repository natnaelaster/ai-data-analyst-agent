from data_agent.profiler import ColumnProfile, DatasetProfile
from data_agent.utils import DataAgentError, ProfilerError, InvalidColumnError, ProfileNotFoundError
from data_agent.profiler import ColumnProfile, DatasetProfile
from data_agent.utils import timed, retry
from data_agent.utils import iter_rows, batched
import pytest

# Test cases for the data_agent package
# Test 1 — DataAgentError
def test_data_agent_error():
    with pytest.raises(DataAgentError) as exc_info: # don't forgate the you are using "exc_info" instead of "e", cause it should attach ".value" for holds metadata wrapping.
        raise DataAgentError("base agent failure")
    
    print(f"Test 1 (DataAgentError): {exc_info.value}")
    assert str(exc_info.value).startswith("[DataAgent]"), "prefix missing"
    
def test_profiler_error():
    with pytest.raises(ProfilerError) as exc_info:
        raise ProfilerError("profile failure")
    
    print(f"Test 2 (ProfilerError): {exc_info.value}")
    # Verify inheritance: ProfilerError should also print [DataAgent]
    assert str(exc_info.value).startswith("[DataAgent]"), "prefix missing"

# Test 3 — InvalidColumnError via ColumnProfile
def test_invalid_column_profile():
    with pytest.raises(InvalidColumnError) as exc_info:
        ColumnProfile("hulu", "int64", -90, 100)

    assert exc_info.value.column_name == "hulu"
    assert exc_info.value.bad_value == -90
    assert str(exc_info.value).startswith("[DataAgent]")

# Test 4 — ProfileNotFoundError via DatasetProfile
profile = DatasetProfile()

def test_profile_missing():
    with pytest.raises(ProfileNotFoundError) as exc_info:
        profile ["missing column"]
    
    assert exc_info.value.column_name == "missing column"
    
if __name__ == "__main__":
    # Test 4 — ProfileNotFoundError via DatasetProfile
    profile = DatasetProfile()
    
    try:
        profile["missing_column"]
    except ProfileNotFoundError as e:
        assert e.column_name == "missing_column"
    else:
        raise AssertionError("ProfileNotFoundError was not raised")    
    
        
    # retry validation fires at decoration time
    try:
        retry(0)
    except ValueError:
        pass
    else:
        raise AssertionError("retry(0) should raise ValueError")

    # batched validation fires on first next(), because it's a generator
    try:
        list(batched(range(3), 0))
    except ValueError:
        pass
    else:
        raise AssertionError("batched size=0 should raise ValueError")

    # null_rates and dirty_columns
    import pandas as pd
    df = pd.DataFrame({"revenue": [100, 200, None], "country": ["ET", "US", "ET"]})
    p = DatasetProfile.from_dataframe(df)
    assert p.dirty_columns == ["revenue"]
    assert abs(p.null_rates["revenue"] - 1/3) < 1e-9    # floats: compare with a tolerance
    assert p.null_rates["country"] == 0

    # the pandas dtype check from earlier
    assert type(p["country"]).__name__ == "CategoricalColumn"