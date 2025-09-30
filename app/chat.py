# app/chat.py

from typing import List, Optional, Dict, Any
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage, AIMessage
from app.tool_manager import ToolManager


class ChatManager:
    """Manages chat sessions with the AI assistant using Ollama."""
    
    def __init__(
        self, 
        model_name: str = "gemma3:4b",
        base_url: str = "http://localhost:11434",
        use_tools: bool = True,
        temperature: float = 0.7
    ):
        self.model_name = model_name
        self.base_url = base_url
        self.use_tools = use_tools
        self.temperature = temperature
        
        # Initialize tool manager
        self.tool_manager = ToolManager()
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize the model and agent
        self._setup_model()
        if self.use_tools and self.tool_manager.get_tools():
            self._setup_agent()
        else:
            self.agent = None
    
    def _setup_model(self) -> None:
        """Sets up the Ollama model."""
        # ChatOllama supports better conversation flow
        self.llm = ChatOllama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=self.temperature
        )
        
        # Fallback to regular Ollama for simpler use cases
        self.simple_llm = Ollama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=self.temperature
        )
    
    def _setup_agent(self) -> None:
        """Sets up the agent with tools."""
        tools = self.tool_manager.get_tools()
        
        if not tools:
            print("No tools available for agent setup.")
            self.agent = None
            return
        
        # Create tool descriptions, tool names, and tools list for the prompt
        tool_descriptions = "\n".join([
            f"- {tool.name}: {tool.description}" 
            for tool in tools
        ])
        tool_names = ", ".join([tool.name for tool in tools])
        # For {tools}, we can pass the tool objects directly or their string representations
        tools_str = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        
        prompt_template = """You are a helpful AI assistant with access to the following tools:
                {tool_descriptions}

                Tool names: {tool_names}

                Tools:
                {tools}

                If the human's input is a greeting, casual conversation, or does not clearly require a tool, respond directly with a conversational answer without using any tools. Only use tools when the input explicitly requires their functionality (e.g., calculations, file operations, or fetching information like time or weather).

                Use this format for tool usage:
                Thought: What do I need to do?
                Action: tool_name
                Action Input: the input to the tool
                Observation: the result of the action
                ... (repeat as needed)
                Thought: I now know the final answer
                Final Answer: the final answer

                Chat history: {chat_history}
                Human: {input}
                {agent_scratchpad}
            """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["input", "chat_history", "agent_scratchpad"],
            partial_variables={
                "tool_descriptions": tool_descriptions,
                "tool_names": tool_names,
                "tools": tools_str
            }
        )
        
        # Create the agent executor
        self.agent_executor = initialize_agent(
            tools=tools,
            llm=self.simple_llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True,
            max_iterations=5  # Optional: limit iterations to avoid infinite loops
        )
    
    def chat(self, message: str) -> str:
        """Process a chat message and return the response."""
        try:
            if self.agent_executor and self.use_tools:
                # Use agent with tools
                response = self.agent_executor.invoke({"input": message})
                return response.get("output", "I couldn't process that request.")
            else:
                # Use simple chat without tools
                messages = self.memory.chat_memory.messages + [HumanMessage(content=message)]
                response = self.llm.invoke(messages)
                
                # Update memory
                self.memory.chat_memory.add_user_message(message)
                self.memory.chat_memory.add_ai_message(response.content)
                
                return response.content
        except Exception as e:
            return f"Error processing message: {str(e)}"
    
    def get_tool_list(self) -> List[str]:
        """Returns a list of available tool names."""
        return self.tool_manager.list_tools()
    
    def reload_tools(self) -> None:
        """Reloads all tools and recreates the agent."""
        self.tool_manager.reload_tools()
        if self.use_tools and self.tool_manager.get_tools():
            self._setup_agent()
    
    def clear_history(self) -> None:
        """Clears the conversation history."""
        self.memory.clear()
    
    def set_model(self, model_name: str) -> None:
        """Changes the model being used."""
        self.model_name = model_name
        self._setup_model()
        if self.use_tools and self.tool_manager.get_tools():
            self._setup_agent()