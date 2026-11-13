"""Extra DataAgent tests: name validation, router branches, empty CSV, repr."""

import tempfile
from pathlib import Path

from data_agent.agent import DataAgent
from data_agent.memory import MemoryStore


def write_csv(text: str) -> Path:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", encoding="utf-8", newline="", delete=False
    ) as file:
        file.write(text)
        return Path(file.name)


def test_name_validation():
    for bad_name in ("", "   ", 5):
        try:
            DataAgent(bad_name, MemoryStore())
        except ValueError:
            pass
        else:
            raise AssertionError(f"name {bad_name!r} should be rejected")


def test_missing_values_route():
    path = write_csv("name,score\nAda,90\nLin,\nSam,70\n")   # score is 1/3 missing
    try:
        agent = DataAgent("analyst", MemoryStore())
        agent.load_data(path)
        answer = agent.respond("any missing values?")
        assert "score" in answer
        assert "name" not in answer                          # name has no nulls
    finally:
        path.unlink()


def test_no_missing_values_route():
    path = write_csv("name,score\nAda,90\nLin,80\n")
    try:
        agent = DataAgent("analyst", MemoryStore())
        agent.load_data(path)
        assert "No column" in agent.respond("null check")
    finally:
        path.unlink()


def test_summary_and_unknown_routes():
    path = write_csv("name,score\nAda,90\nLin,80\n")
    try:
        agent = DataAgent("analyst", MemoryStore())
        agent.load_data(path)
        summary = agent.respond("give me a summary")
        assert "name" in summary and "score" in summary and "mean" in summary
        assert "columns" in agent.respond("what is the weather?")   # falls to the help message
    finally:
        path.unlink()


def test_empty_csv_rejected():
    path = write_csv("name,score\n")                          # header only
    try:
        agent = DataAgent("analyst", MemoryStore())
        try:
            agent.load_data(path)
        except ValueError:
            pass
        else:
            raise AssertionError("a CSV with no rows should be rejected")
    finally:
        path.unlink()


def test_repr_works_with_minimal_memory():
    class StoreOnly:                                          # no __len__ on purpose
        def store(self, key, value): ...
        def retrieve(self, key): ...

    assert "data_loaded=False" in repr(DataAgent("analyst", StoreOnly()))

    path = write_csv("name,score\nAda,90\n")
    try:
        agent = DataAgent("analyst", MemoryStore())
        agent.load_data(path)
        assert "data_loaded=True" in repr(agent)
        assert "memory_items=1" in repr(agent)                # "last_file" was remembered
    finally:
        path.unlink()


if __name__ == "__main__":
    test_name_validation()
    test_missing_values_route()
    test_no_missing_values_route()
    test_summary_and_unknown_routes()
    test_empty_csv_rejected()
    test_repr_works_with_minimal_memory()
    print("all extra tests passed")