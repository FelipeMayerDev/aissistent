from langchain.tools import tool

@tool
def get_current_time(_: str = "") -> str:
    """Returns the current date and time as a string in format YYYY-MM-DD HH:MM:SS."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")