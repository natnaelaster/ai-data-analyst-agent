import pandas as pd
import csv
import time
from data_agent.utils import DataAgentError, timed, retry, iter_rows, batched
from data_agent.profiler import ColumnProfile, DatasetProfile

if __name__ == "__main__":
    '''
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
        print(f"Test 3 (InvalidColumnError): {e}")
        # Verify the attributes are accessible
        print(f"  column_name = {e.column_name}")
        print(f"  bad_value   = {e.bad_value}")

    # Test 4 — ProfileNotFoundError via DatasetProfile
    profile = DatasetProfile()
    try:
        profile["missing_column"]
    except ProfileNotFoundError as e:
        print(f"Test 4 (ProfileNotFoundError): {e}")
        print(f"  column_name = {e.column_name}")
    '''    
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
