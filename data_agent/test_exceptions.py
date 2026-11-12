from data_agent.profiler import ColumnProfile, DatasetProfile
from data_agent.utils import DataAgentError, ProfilerError, InvalidColumnError, ProfileNotFoundError
from data_agent.profiler import ColumnProfile, DatasetProfile
from data_agent.utils import timed, retry
from data_agent.utils import iter_rows, batched

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