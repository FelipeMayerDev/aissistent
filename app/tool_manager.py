import os
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Any, Callable
from langchain.tools import Tool, StructuredTool
from pydantic.v1 import BaseModel, Field, validator


class ToolManager:
    """Manages dynamic loading and registration of tools for the AI assistant."""
    
    def __init__(self, tools_dir: str = "tools"):
        self.tools_dir = Path(tools_dir)
        self.tools: Dict[str, Tool] = {}
        self.load_tools()
    
    def load_tools(self) -> None:
        """Dynamically loads all tools from the tools directory."""
        if not self.tools_dir.exists():
            print(f"Warning: Tools directory '{self.tools_dir}' does not exist.")
            return
        
        # Get all Python files in the tools directory
        tool_files = self.tools_dir.glob("*.py")
        
        for tool_file in tool_files:
            if tool_file.name.startswith("__"):
                continue
                
            try:
                self._load_tool_from_file(tool_file)
            except Exception as e:
                print(f"Error loading tool from {tool_file}: {e}")
    
    def _load_tool_from_file(self, file_path: Path) -> None:
        """Loads a tool from a Python file."""
        module_name = file_path.stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for tool definitions in the module
            for name, obj in inspect.getmembers(module):
                if self._is_tool(obj):
                    self._register_tool(name, obj)
                elif self._is_tool_function(obj):
                    # Convert function to Tool
                    tool = self._create_tool_from_function(name, obj)
                    if tool:
                        self._register_tool(name, tool)
    
    def _is_tool(self, obj: Any) -> bool:
        """Checks if an object is a LangChain Tool."""
        return isinstance(obj, (Tool, StructuredTool))
    
    def _is_tool_function(self, obj: Any) -> bool:
        """Checks if an object is a callable that can be converted to a tool."""
        return (
            callable(obj) 
            and hasattr(obj, '__name__') 
            and not obj.__name__.startswith('_')
            and hasattr(obj, '_is_tool') and obj._is_tool
        )
    
    def _create_tool_from_function(self, name: str, func: Callable) -> Tool:
        """Creates a LangChain Tool from a decorated function."""
        # Extract metadata from the function
        description = func.__doc__ or f"Tool: {name}"
        
        return Tool(
            name=name,
            description=description.strip(),
            func=func
        )
    
    def _register_tool(self, name: str, tool: Tool) -> None:
        """Registers a tool in the manager."""
        self.tools[name] = tool
        print(f"Loaded tool: {name}")
    
    def get_tools(self) -> List[Tool]:
        """Returns a list of all loaded tools."""
        return list(self.tools.values())
    
    def get_tool(self, name: str) -> Tool:
        """Returns a specific tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """Returns a list of all tool names."""
        return list(self.tools.keys())
    
    def reload_tools(self) -> None:
        """Reloads all tools from the tools directory."""
        self.tools.clear()
        self.load_tools()


def tool(func: Callable) -> Callable:
    """Decorator to mark a function as a tool."""
    func._is_tool = True
    return func