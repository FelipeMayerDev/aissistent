from langchain.tools import StructuredTool
import os
from pydantic import BaseModel, Field

class WriteFileInput(BaseModel):
    path: str = Field(description="Path to the file to write")
    content: str = Field(description="Content to write to the file")

class ReadFileInput(BaseModel):
    path: str = Field(description="Path to the file to read")

def read_file(path: str) -> str:
    try:
        if not os.path.exists(path):
            return f"File {path} not found"
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file_wrapper(path: str, content: str) -> str:  # Fixed: Added content parameter
    """Wrapper for writing to a file without Pydantic validation."""
    try:
        # Basic input validation (optional)
        if not isinstance(path, str) or not isinstance(content, str):
            return "Error: Path and content must be strings"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

file_reader = StructuredTool.from_function(
    func=read_file,
    name="read_file",
    description="Reads the content of a file given a path",
    args_schema=ReadFileInput
)

file_writer_wrapper_tool = StructuredTool.from_function(
    func=write_file_wrapper,
    name="write_file_wrapper",
    description="Creates or overwrites a file at the given path and writes content to it if needed",
    args_schema=WriteFileInput
)