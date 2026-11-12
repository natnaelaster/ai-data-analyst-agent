import tempfile
import uuid
from pathlib import Path

from data_agent.agent import DataAgent
from data_agent.utils import DataNotLoadedError, MemoryNotFoundError


class TinyMemory:
    """A small test double that implements the agent's memory interface."""

    def __init__(self):
        self.items = {}

    def store(self, key, value):
        self.items[key] = value

    def retrieve(self, key):
        try:
            return self.items[key]
        except KeyError:
            raise MemoryNotFoundError("Memory key not found", key) from None


def make_agent(memory=None):
    return DataAgent("analyst", memory if memory is not None else TinyMemory())


def write_csv():
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", encoding="utf-8", newline="", delete=False
    ) as file:
        file.write("name,age\nAda,36\nLin,31\n")
        return Path(file.name)


def test_errors_and_loading():
    agent = make_agent()

    try:
        agent.respond("which columns")
    except DataNotLoadedError:
        pass
    else:
        raise AssertionError("respond() should require loaded data")

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as file:
        txt_path = Path(file.name)
    try:
        try:
            agent.load_data(txt_path)
        except ValueError:
            pass
        else:
            raise AssertionError("load_data() should reject .txt files")
    finally:
        txt_path.unlink()

    missing_path = Path(tempfile.gettempdir()) / f"{uuid.uuid4().hex}.csv"
    try:
        agent.load_data(missing_path)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("load_data() should reject missing files")


def test_columns_and_recall():
    path = write_csv()
    try:
        agent = make_agent()
        agent.load_data(path)

        answer = agent.respond("which columns").lower()
        assert "name" in answer
        assert "age" in answer
        assert agent.recall("last_file") == str(path)

        try:
            agent.recall("nope")
        except MemoryNotFoundError:
            pass
        else:
            raise AssertionError("recall() should reject unknown keys")
    finally:
        path.unlink()


def test_history_is_a_copy():
    path = write_csv()
    try:
        agent = make_agent()
        agent.load_data(path)
        agent.respond("which columns")
        agent.respond("summary")

        assert len(agent.history) == 2
        returned_history = agent.history
        returned_history.clear()
        assert len(agent.history) == 2
    finally:
        path.unlink()


def test_custom_memory_object():
    memory = TinyMemory()
    agent = make_agent(memory)

    agent.remember("example", "stored value")
    assert agent.recall("example") == "stored value"


if __name__ == "__main__":
    test_errors_and_loading()
    test_columns_and_recall()
    test_history_is_a_copy()
    test_custom_memory_object()