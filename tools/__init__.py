"""
Tools package for AI Agent
This package contains all available tools/functions that the AI agent can use.
Each tool should be in its own module and registered through the ToolRegistry.
"""

from .base_tool import BaseTool, ToolRegistry
from .task_tools import CreateMindTaskTool, CreateBodyTaskTool
from .query_tools import GetUserTasksTool, GetUserStatsTool
from .template_tools import GetTaskTemplatesTool

__all__ = [
    'BaseTool',
    'ToolRegistry',
    'CreateMindTaskTool',
    'CreateBodyTaskTool',
    'GetUserTasksTool',
    'GetUserStatsTool',
    'GetTaskTemplatesTool',
]
