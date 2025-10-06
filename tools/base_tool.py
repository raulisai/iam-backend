"""
Base classes for AI Agent tools
Provides a framework for creating reusable, composable tools
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from lib.agent import AIAgent

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """
    Base class for all agent tools
    Each tool should inherit from this class and implement the required methods
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for the tool"""
        ...
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does"""
        ...
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON schema for the tool's parameters"""
        ...
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool's action
        
        Args:
            **kwargs: Parameters defined in the parameters schema
            
        Returns:
            Dict with result information (should include 'success' key)
        """
        ...
    
    def validate_params(self, **kwargs) -> bool:  # noqa: ARG002
        """
        Optional: Validate parameters before execution
        Override this method if you need custom validation
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return True
    
    def on_error(self, error: Exception) -> Dict[str, Any]:
        """
        Handle errors that occur during execution
        Override this method for custom error handling
        
        Args:
            error: The exception that occurred
            
        Returns:
            Dict with error information
        """
        logger.error("Error in tool '%s': %s", self.name, str(error))
        return {
            "success": False,
            "error": str(error),
            "tool": self.name
        }


class ToolRegistry:
    """
    Registry for managing and registering tools with the AI agent
    Provides auto-discovery and registration of tools
    """
    
    def __init__(self, agent: AIAgent):
        """
        Initialize the tool registry
        
        Args:
            agent: The AI agent to register tools with
        """
        self.agent = agent
        self.tools: Dict[str, BaseTool] = {}
        logger.info("Tool registry initialized")
    
    def register_tool(self, tool: BaseTool) -> None:
        """
        Register a single tool with the agent
        
        Args:
            tool: Instance of a BaseTool subclass
        """
        try:
            # Create a wrapper function that calls the tool's execute method
            def tool_wrapper(**kwargs):
                try:
                    if not tool.validate_params(**kwargs):
                        return {
                            "success": False,
                            "error": "Invalid parameters",
                            "tool": tool.name
                        }
                    return tool.execute(**kwargs)
                except Exception as e:  # noqa: BLE001
                    return tool.on_error(e)
            
            # Register with the agent
            self.agent.register_function(
                name=tool.name,
                description=tool.description,
                parameters=tool.parameters
            )(tool_wrapper)
            
            # Store in registry
            self.tools[tool.name] = tool
            logger.info("Registered tool: %s", tool.name)
            
        except Exception as e:
            logger.error("Failed to register tool '%s': %s", tool.name, str(e))
            raise
    
    def register_tools(self, tools: List[BaseTool]) -> None:
        """
        Register multiple tools at once
        
        Args:
            tools: List of BaseTool instances
        """
        for tool in tools:
            self.register_tool(tool)
        logger.info("Registered %d tools", len(tools))
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Get a registered tool by name
        
        Args:
            name: Name of the tool
            
        Returns:
            BaseTool instance or None if not found
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """
        List all registered tool names
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all registered tools
        
        Returns:
            List of dicts with tool information
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools.values()
        ]
