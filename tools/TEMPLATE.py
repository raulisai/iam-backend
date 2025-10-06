"""
TEMPLATE: Use this as a starting point for creating new tools
Copy this file and modify it for your specific tool needs
"""

import logging
from typing import Dict, Any
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)


class YourToolNameHere(BaseTool):
    """
    Brief description of what your tool does
    
    This tool allows the agent to... [explain the capability]
    """
    
    @property
    def name(self) -> str:
        """
        Unique identifier for the tool
        Use snake_case: create_goal, get_profile, send_notification, etc.
        """
        return "your_tool_name"
    
    @property
    def description(self) -> str:
        """
        Detailed description that helps the AI decide WHEN to use this tool
        
        Be specific about:
        - What the tool does
        - When it should be used
        - What kind of user requests trigger it
        - Any prerequisites or dependencies
        """
        return """Your detailed description here.
        
Use this tool when:
- The user asks about X
- The user wants to do Y
- You need to accomplish Z

Example scenarios:
- "User says: I want to..."
- "User says: Can you...?"
"""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """
        JSON Schema defining the tool's parameters
        
        Follow OpenAI's function calling schema format:
        https://platform.openai.com/docs/guides/function-calling
        """
        return {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",  # string, integer, number, boolean, array, object
                    "description": "Clear description of what this parameter is for",
                    # Optional constraints:
                    # "enum": ["option1", "option2"],
                    # "minimum": 1,
                    # "maximum": 100,
                    # "default": "default_value"
                },
                "param2": {
                    "type": "integer",
                    "description": "Another parameter example",
                    "minimum": 0
                },
                "optional_param": {
                    "type": "string",
                    "description": "This parameter is optional"
                }
            },
            "required": ["param1", "param2"]  # List required parameters
        }
    
    def validate_params(self, **kwargs) -> bool:
        """
        Optional: Add custom validation logic here
        
        This runs BEFORE execute() and can prevent execution if params are invalid.
        Return True if valid, False if invalid.
        
        If you don't need custom validation, you can remove this method.
        """
        param1 = kwargs.get('param1')
        param2 = kwargs.get('param2')
        
        # Example validation
        if not param1 or len(param1) < 3:
            logger.warning(f"Invalid param1: {param1}")
            return False
        
        if param2 < 0:
            logger.warning(f"Invalid param2: {param2}")
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Main execution logic for the tool
        
        This is where you implement what the tool actually does.
        
        Args:
            **kwargs: Parameters as defined in the parameters schema
        
        Returns:
            Dict with at least:
            - "success": bool - Whether the operation succeeded
            - "message": str - User-friendly message about what happened
            - ... any other relevant data
        """
        try:
            # 1. Extract parameters
            param1 = kwargs.get('param1')
            param2 = kwargs.get('param2')
            optional_param = kwargs.get('optional_param', 'default_value')
            
            # 2. Perform your business logic here
            # Call services, make database queries, process data, etc.
            # Example:
            # from services.your_service import your_function
            # result = your_function(param1, param2)
            
            result = self._your_helper_method(param1, param2)
            
            # 3. Log the action
            logger.info(f"Tool {self.name} executed successfully: {param1}, {param2}")
            
            # 4. Return success response
            return {
                "success": True,
                "result": result,
                "message": f"Successfully completed the operation!",
                # Add any other relevant data:
                "param1_used": param1,
                "param2_used": param2
            }
            
        except Exception as e:
            # Errors are automatically handled by on_error()
            # But you can do custom error handling here if needed
            logger.error(f"Error in {self.name}: {str(e)}")
            raise
    
    def _your_helper_method(self, param1, param2):
        """
        Optional: Add helper methods as needed
        Use underscore prefix for private methods
        """
        # Your logic here
        return f"Processed {param1} with {param2}"
    
    def on_error(self, error: Exception) -> Dict[str, Any]:
        """
        Optional: Custom error handling
        
        Override this if you want special error handling.
        Otherwise, the default from BaseTool will be used.
        """
        logger.error(f"Custom error handler for {self.name}: {str(error)}")
        
        # You can return a custom error response
        return {
            "success": False,
            "error": str(error),
            "tool": self.name,
            "message": "Sorry, something went wrong. Please try again."
        }


# ============================================================================
# HOW TO USE THIS TEMPLATE:
# ============================================================================
# 
# 1. Copy this file to a new file in the tools/ directory
#    Example: tools/notification_tools.py
# 
# 2. Rename the class to something meaningful
#    Example: SendNotificationTool, CreateGoalTool, etc.
# 
# 3. Update the name, description, and parameters properties
# 
# 4. Implement the execute() method with your business logic
# 
# 5. Add your tool to tools/__init__.py:
#    from .notification_tools import SendNotificationTool
#    __all__ = [..., 'SendNotificationTool']
# 
# 6. Register in services/agent_service.py:
#    from tools import SendNotificationTool
#    tools = [..., SendNotificationTool()]
# 
# 7. Test your tool!
# 
# ============================================================================


# Example of a simple tool without validation:
class SimpleExampleTool(BaseTool):
    """A minimal example tool"""
    
    @property
    def name(self) -> str:
        return "simple_example"
    
    @property
    def description(self) -> str:
        return "A simple example tool that echoes back the input"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to echo"
                }
            },
            "required": ["message"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        message = kwargs.get('message')
        return {
            "success": True,
            "echo": message,
            "message": f"Echoing: {message}"
        }
