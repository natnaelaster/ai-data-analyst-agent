from data_agent.utils.validators import validate_null_count

class ColumnProfile:
    def __init__(self, name, dtype, null_count, total_count):
        validate_null_count(null_count, total_count)  # ← one line, logic lives elsewhere
        self.name = name
        ...