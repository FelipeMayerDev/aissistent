from app.tool_manager import tool
import math


@tool
def calculate(expression: str) -> str:
    """
    Performs mathematical calculations.
    Args:
        expression: A mathematical expression to evaluate
    Returns:
        The result of the calculation
    """
    try:
        # Safe evaluation of mathematical expressions
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

