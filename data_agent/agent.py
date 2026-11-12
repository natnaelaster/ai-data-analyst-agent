from data_agent.utils import timed

class DataAgent:
    def __init__(self, name: str, memory):
        # name must be a non-empty string (ValueError, with the bad value in the message)
        # self.memory = memory      (received, not created)
        # self.profile = None       (set when data is loaded)
        # self._history = []        (list of (query, answer) tuples)
        return f"place holder for DataAgent(name={name!r}, memory={memory!r})"

    @timed
    def load_data(self, filepath: Path) -> None:
        # 1. suffix must be ".csv", otherwise ValueError (Path.suffix)
        # 2. file must exist, otherwise FileNotFoundError (Path.exists)
        # 3. read with pandas, build self.profile with DatasetProfile.from_dataframe
        # 4. remember("last_file", str(filepath))
        return f"place holder for load_data(filepath={filepath!r})"

    def remember(self, key: str, value) -> None: ...   # delegates to memory.store
    def recall(self, key: str): ...                    # delegates to memory.retrieve

    def respond(self, query: str) -> str:
        # raises DataNotLoadedError if self.profile is None
        # lowercase the query, then route by keyword:
        #   "column"           -> names of all columns
        #   "null" / "missing" -> the dirty_columns, with their null_rates
        #   "summary"          -> each column's summary() joined by newlines
        #   anything else      -> a short message listing what you can answer
        # append (query, answer) to self._history, then return the answer
        return f"place holder for respond(query={query!r})"

    @property
    def history(self) -> list: ...      # return list(self._history), a copy

    def __repr__(self) -> str: ...      # DataAgent(name='analyst', data_loaded=True, memory_items=2)