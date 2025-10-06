"""
Task creation tools for the AI Agent
Tools for creating mind and body tasks
"""

import logging
from typing import Dict, Any
from datetime import datetime, timezone
from .base_tool import BaseTool
from services.mind_task_service import create_mind_task
from services.body_task_service import create_body_task

logger = logging.getLogger(__name__)


class CreateMindTaskTool(BaseTool):
    """Tool for creating mental/cognitive tasks"""
    
    @property
    def name(self) -> str:
        return "create_mind_task"
    
    @property
    def description(self) -> str:
        return """Create a mental/cognitive task for the user based on a template.
        
Use this tool when recommending or creating tasks related to:
- Reading, studying, or learning
- Planning and organizing
- Meditation and mindfulness
- Journaling or writing
- Problem-solving activities
- Creative thinking exercises
- Memory training
- Any cognitive or intellectual activity

IMPORTANT: Tasks are created from templates. You must provide a template_id.
Common template IDs for mind tasks:
- 'meditation' for meditation sessions
- 'reading' for reading activities
- 'journaling' for writing/reflection
- 'planning' for organization tasks

The task will be automatically added to the user's mind tasks list."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user for whom to create the task"
                },
                "template_key": {
                    "type": "string",
                    "description": "The task template key (e.g., 'meditation_15', 'daily_reading_01', 'journal_writing_01'). Get available keys from get_task_templates tool."
                },
                "scheduled_at": {
                    "type": "string",
                    "description": "When to schedule the task (ISO datetime format). If not provided, defaults to current time."
                },
                "params": {
                    "type": "object",
                    "description": "Custom parameters for the task. Common params: {'duration': 30, 'notes': 'morning session', 'goal': 'relax'}"
                }
            },
            "required": ["user_id", "template_key"]
        }
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters before execution"""
        user_id = kwargs.get('user_id')
        template_key = kwargs.get('template_key')
        
        logger.debug("CreateMindTaskTool validating: user_id=%s, template_key=%s, all_kwargs=%s", user_id, template_key, kwargs)
        
        if not user_id or not isinstance(user_id, str):
            logger.warning("Invalid user_id: %s", user_id)
            return False
        
        if not template_key or not isinstance(template_key, str):
            logger.warning("Invalid template_key: %s (type: %s), received kwargs: %s", template_key, type(template_key).__name__, list(kwargs.keys()))
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Create a mind task"""
        try:
            from services.task_template_service import get_task_template_by_key
            
            user_id = kwargs.get('user_id')
            template_key = kwargs.get('template_key')
            scheduled_at = kwargs.get('scheduled_at')
            params = kwargs.get('params', {})
            
            # Convert template_key to template_id (UUID)
            template = get_task_template_by_key(template_key)
            if not template:
                logger.error("Template not found: %s", template_key)
                return {
                    "success": False,
                    "error": f"Template '{template_key}' not found",
                    "message": f"Task template '{template_key}' does not exist. Use get_task_templates to see available templates."
                }
            
            template_id = template.get('id')
            
            # Prepare task data according to database schema
            task_data = {
                "user_id": user_id,
                "template_id": template_id,
                "created_by": "bot",
                "status": "pending",
                "scheduled_at": scheduled_at or datetime.now(timezone.utc).isoformat(),
                "params": params
            }
            
            # Create the task
            task = create_mind_task(task_data)
            
            logger.info("Mind task created via agent tool: %s (template: %s) for user %s", task.get('id'), template_key, user_id)
            
            return {
                "success": True,
                "task_id": task.get('id'),
                "task_type": "mind",
                "template_key": template_key,
                "template_name": template.get('name'),
                "scheduled_at": task_data["scheduled_at"],
                "message": "✅ Mental task has been added to your list! Complete it to earn XP."
            }
            
        except Exception as e:  # noqa: BLE001
            logger.error("Error creating mind task: %s", str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create mind task. Please try again."
            }


class CreateBodyTaskTool(BaseTool):
    """Tool for creating physical/body tasks"""
    
    @property
    def name(self) -> str:
        return "create_body_task"
    
    @property
    def description(self) -> str:
        return """Create a physical/body task for the user based on a template.
        
Use this tool when recommending or creating tasks related to:
- Exercise and workouts (running, gym, swimming, etc.)
- Yoga and stretching
- Sports activities
- Walking or hiking
- Dance or movement
- Physical therapy exercises
- Breathing exercises
- Any physical or body-related activity

IMPORTANT: Tasks are created from templates. You must provide a template_id.
Common template IDs for body tasks:
- 'workout' for general exercise
- 'running' for running activities
- 'yoga' for yoga sessions
- 'stretching' for flexibility work

The task will be automatically added to the user's body tasks list."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user for whom to create the task"
                },
                "template_key": {
                    "type": "string",
                    "description": "The task template key (e.g., 'morning_run_01', 'strength_training_01'). Get available keys from get_task_templates tool."
                },
                "scheduled_at": {
                    "type": "string",
                    "description": "When to schedule the task (ISO datetime format). If not provided, defaults to current time."
                },
                "params": {
                    "type": "object",
                    "description": "Custom parameters for the task. Common params: {'reps': 10, 'sets': 3, 'weight': 20, 'distance_km': 5}"
                }
            },
            "required": ["user_id", "template_key"]
        }
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters before execution"""
        user_id = kwargs.get('user_id')
        template_key = kwargs.get('template_key')
        
        logger.debug("CreateBodyTaskTool validating: user_id=%s, template_key=%s, all_kwargs=%s", user_id, template_key, kwargs)
        
        if not user_id or not isinstance(user_id, str):
            logger.warning("Invalid user_id: %s", user_id)
            return False
        
        if not template_key or not isinstance(template_key, str):
            logger.warning("Invalid template_key: %s (type: %s), received kwargs: %s", template_key, type(template_key).__name__, list(kwargs.keys()))
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Create a body task"""
        try:
            from services.task_template_service import get_task_template_by_key
            
            user_id = kwargs.get('user_id')
            template_key = kwargs.get('template_key')
            scheduled_at = kwargs.get('scheduled_at')
            params = kwargs.get('params', {})
            
            # Convert template_key to template_id (UUID)
            template = get_task_template_by_key(template_key)
            if not template:
                logger.error("Template not found: %s", template_key)
                return {
                    "success": False,
                    "error": f"Template '{template_key}' not found",
                    "message": f"Task template '{template_key}' does not exist. Use get_task_templates to see available templates."
                }
            
            template_id = template.get('id')
            
            # Prepare task data according to database schema
            task_data = {
                "user_id": user_id,
                "template_id": template_id,
                "created_by": "bot",
                "status": "pending",
                "scheduled_at": scheduled_at or datetime.now(timezone.utc).isoformat(),
                "params": params
            }
            
            # Create the task
            task = create_body_task(task_data)
            
            logger.info("Body task created via agent tool: %s (template: %s) for user %s", task.get('id'), template_key, user_id)
            
            return {
                "success": True,
                "task_id": task.get('id'),
                "task_type": "body",
                "template_key": template_key,
                "template_name": template.get('name'),
                "scheduled_at": task_data["scheduled_at"],
                "message": "✅ Physical task has been added to your list! Complete it to earn XP."
            }
            
        except Exception as e:  # noqa: BLE001
            logger.error("Error creating body task: %s", str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create body task. Please try again."
            }
