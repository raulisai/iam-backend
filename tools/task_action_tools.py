"""
Task action tools for the AI Agent
Tools for completing, updating, and managing tasks
"""

import logging
from typing import Dict, Any
from .base_tool import BaseTool
from services.mind_task_service import (
    complete_mind_task, 
    update_mind_task, 
    get_mind_task_by_id
)
from services.body_task_service import (
    complete_body_task, 
    update_body_task, 
    get_body_task_by_id
)

logger = logging.getLogger(__name__)


class CompleteTaskTool(BaseTool):
    """Tool for marking tasks as completed"""
    
    @property
    def name(self) -> str:
        return "complete_task"
    
    @property
    def description(self) -> str:
        return """Mark a task as completed and award XP to the user.
        
Use this tool when the user indicates they:
- Completed a task
- Finished an activity
- "I did the meditation"
- "Just finished my workout"
- Want to check off a task

IMPORTANT: You need the task_id to complete a task. If you don't have it,
use get_user_tasks first to find the task."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task to complete"
                },
                "task_type": {
                    "type": "string",
                    "enum": ["mind", "body"],
                    "description": "Type of task: 'mind' or 'body'"
                },
                "xp_awarded": {
                    "type": "integer",
                    "description": "XP to award (usually the task's original xp_reward). If not provided, will use the task's xp_reward value.",
                    "minimum": 0
                }
            },
            "required": ["task_id", "task_type"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Complete a task"""
        try:
            task_id = kwargs.get('task_id')
            task_type = kwargs.get('task_type')
            xp_awarded = kwargs.get('xp_awarded')
            
            # Get task to check if it exists and get XP if not provided
            if task_type == 'mind':
                task = get_mind_task_by_id(task_id)
                if not task:
                    return {
                        "success": False,
                        "message": "Mind task not found."
                    }
                
                # Use task's xp_reward if not provided
                if xp_awarded is None:
                    xp_awarded = task.get('xp_reward', 0)
                
                # Complete the task
                updated_task = complete_mind_task(task_id, xp_awarded)
                
            elif task_type == 'body':
                task = get_body_task_by_id(task_id)
                if not task:
                    return {
                        "success": False,
                        "message": "Body task not found."
                    }
                
                # Use task's xp_reward if not provided
                if xp_awarded is None:
                    xp_awarded = task.get('xp_reward', 0)
                
                # Complete the task
                updated_task = complete_body_task(task_id, xp_awarded)
            else:
                return {
                    "success": False,
                    "message": "Invalid task type. Must be 'mind' or 'body'."
                }
            
            task_title = updated_task.get('title', 'Task')
            
            logger.info(f"Task completed via agent: {task_id} ({task_type}) - {xp_awarded} XP awarded")
            
            return {
                "success": True,
                "task_id": task_id,
                "task_type": task_type,
                "task_title": task_title,
                "xp_awarded": xp_awarded,
                "message": f"🎉 Congratulations! You completed '{task_title}' and earned {xp_awarded} XP!"
            }
            
        except Exception as e:
            logger.error(f"Error completing task: {str(e)}")
            raise


class UpdateTaskTool(BaseTool):
    """Tool for updating task details"""
    
    @property
    def name(self) -> str:
        return "update_task"
    
    @property
    def description(self) -> str:
        return """Update details of an existing task.
        
Use this tool when the user wants to:
- Change a task's title or description
- Modify priority
- Update estimated duration
- Adjust XP reward
- Make any changes to an existing task

IMPORTANT: You need the task_id to update a task. If you don't have it,
use get_user_tasks first to find the task."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task to update"
                },
                "task_type": {
                    "type": "string",
                    "enum": ["mind", "body"],
                    "description": "Type of task: 'mind' or 'body'"
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task"
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "New priority level"
                },
                "xp_reward": {
                    "type": "integer",
                    "description": "New XP reward value",
                    "minimum": 10,
                    "maximum": 100
                },
                "estimated_duration": {
                    "type": "integer",
                    "description": "New estimated duration in minutes",
                    "minimum": 1
                }
            },
            "required": ["task_id", "task_type"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Update a task"""
        try:
            task_id = kwargs.get('task_id')
            task_type = kwargs.get('task_type')
            
            # Build update data from provided kwargs
            update_data = {}
            for key in ['title', 'description', 'priority', 'xp_reward', 'estimated_duration']:
                if key in kwargs and kwargs[key] is not None:
                    update_data[key] = kwargs[key]
            
            if not update_data:
                return {
                    "success": False,
                    "message": "No fields to update were provided."
                }
            
            # Update the task
            if task_type == 'mind':
                updated_task = update_mind_task(task_id, update_data)
            elif task_type == 'body':
                updated_task = update_body_task(task_id, update_data)
            else:
                return {
                    "success": False,
                    "message": "Invalid task type. Must be 'mind' or 'body'."
                }
            
            if not updated_task:
                return {
                    "success": False,
                    "message": f"Could not update {task_type} task. Task may not exist."
                }
            
            updated_fields = list(update_data.keys())
            task_title = updated_task.get('title', 'Task')
            
            logger.info(f"Task updated via agent: {task_id} ({task_type}) - Fields: {updated_fields}")
            
            return {
                "success": True,
                "task_id": task_id,
                "task_type": task_type,
                "updated_fields": updated_fields,
                "task": updated_task,
                "message": f"✅ Task '{task_title}' has been updated successfully!"
            }
            
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            raise
