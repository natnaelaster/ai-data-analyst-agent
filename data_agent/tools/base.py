class BaseTool:
    """Placeholder for the base tool class.

    Every concrete tool (web search, calculator, Python REPL, etc.)
    will inherit from this. Currently empty on purpose.
    """
    def __repr__(self):
        return "BaseTool(empty — placeholder)"
    
if __name__ == "__main__":
    tool = BaseTool()
    print(tool)
    