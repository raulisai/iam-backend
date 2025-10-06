"""
Task Template tools for the AI Agent
Tools for querying and working with task templates
"""

import logging
from typing import Dict, Any
from .base_tool import BaseTool
from services.task_template_service import get_all_task_templates

logger = logging.getLogger(__name__)


class GetTaskTemplatesTool(BaseTool):
    """Tool for getting available task templates"""
    
    @property
    def name(self) -> str:
        return "get_task_templates"
    
    @property
    def description(self) -> str:
        return """Get all available task templates (mind and body).
        
Use this tool to:
- Find template IDs before creating tasks
- Browse available task types
- Get information about template categories, difficulty, XP rewards, and estimated durations

Templates contain the base configuration for tasks like meditation, exercise, reading, etc.
Each template has a unique 'key' which is used as the template_id when creating tasks."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["mind", "body", "all"],
                    "description": "Filter templates by category. 'mind' for mental tasks, 'body' for physical tasks, 'all' for both.",
                    "default": "all"
                }
            }
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Get task templates"""
        try:
            category = kwargs.get('category', 'all')
            
            # Get all templates
            templates = get_all_task_templates()
            
            # Filter by category if specified
            if category != 'all':
                templates = [t for t in templates if t.get('category') == category]
            
            # Format templates for easy understanding
            formatted_templates = []
            for template in templates:
                formatted_templates.append({
                    "template_key": template.get('key'),  # This is what you use to create tasks (e.g., 'meditation_15')
                    "template_id": template.get('id'),  # UUID (internal use)
                    "name": template.get('name'),
                    "category": template.get('category'),
                    "difficulty": template.get('difficulty'),
                    "reward_xp": template.get('reward_xp'),
                    "estimated_minutes": template.get('estimated_minutes'),
                    "description": template.get('descr', ''),
                    "default_params": template.get('default_params', {})
                })
            
            logger.info("Retrieved %d task templates (category: %s)", len(formatted_templates), category)
            
            return {
                "success": True,
                "count": len(formatted_templates),
                "templates": formatted_templates,
                "message": f"Found {len(formatted_templates)} {category} task templates"
            }
            
        except Exception as e:  # noqa: BLE001
            logger.error("Error getting task templates: %s", str(e))
            return {
                "success": False,
                "error": str(e),
                "templates": [],
                "message": "Failed to retrieve task templates"
            }
