if __name__ == "__main__":
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
    from data_agent.profiler.dataset import DatasetProfile
    profile = DatasetProfile()
    try:
        profile["missing_column"]
    except ProfileNotFoundError as e:
        print(f"Test 4 (ProfileNotFoundError): {e}")
        print(f"  column_name = {e.column_name}")