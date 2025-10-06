"""
Query tools for the AI Agent
Tools for retrieving information about tasks, stats, etc.
"""

import logging
from typing import Dict, Any
from .base_tool import BaseTool
from services.mind_task_service import get_user_mind_tasks
from services.body_task_service import get_user_body_tasks
from services.profile_service import get_profile_by_user_id
from services.stats_service import get_latest_snapshot, get_stats_summary

logger = logging.getLogger(__name__)


class GetUserTasksTool(BaseTool):
    """Tool for retrieving user's tasks"""
    
    @property
    def name(self) -> str:
        return "get_user_tasks"
    
    @property
    def description(self) -> str:
        return """Get the user's current tasks (mind and/or body tasks).
        
Use this tool when the user asks about:
- "What tasks do I have?"
- "Show me my pending tasks"
- "What's on my to-do list?"
- "Do I have any tasks today?"
- Checking progress or reviewing their task list

This helps you provide personalized recommendations based on what they already have."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user"
                },
                "task_type": {
                    "type": "string",
                    "enum": ["mind", "body", "both"],
                    "description": "Type of tasks to retrieve: 'mind' for mental tasks, 'body' for physical tasks, 'both' for all tasks",
                    "default": "both"
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "completed", "all"],
                    "description": "Filter by status: 'pending', 'completed', or 'all'",
                    "default": "pending"
                }
            },
            "required": ["user_id"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Get user's tasks"""
        try:
            user_id = kwargs.get('user_id')
            task_type = kwargs.get('task_type', 'both')
            status = kwargs.get('status', 'pending')
            
            # Convert status filter
            status_filter = None if status == 'all' else status
            
            tasks = {
                "mind_tasks": [],
                "body_tasks": []
            }
            
            # Get mind tasks
            if task_type in ['mind', 'both']:
                mind_tasks = get_user_mind_tasks(user_id, status_filter)
                tasks["mind_tasks"] = mind_tasks or []
            
            # Get body tasks
            if task_type in ['body', 'both']:
                body_tasks = get_user_body_tasks(user_id, status_filter)
                tasks["body_tasks"] = body_tasks or []
            
            total_tasks = len(tasks["mind_tasks"]) + len(tasks["body_tasks"])
            
            # Build a friendly summary
            summary_parts = []
            if tasks["mind_tasks"]:
                summary_parts.append(f"{len(tasks['mind_tasks'])} mental task(s)")
            if tasks["body_tasks"]:
                summary_parts.append(f"{len(tasks['body_tasks'])} physical task(s)")
            
            summary = " and ".join(summary_parts) if summary_parts else "no tasks"
            
            logger.info("Retrieved tasks for user %s: %s", user_id, summary)
            
            return {
                "success": True,
                "total_tasks": total_tasks,
                "mind_tasks_count": len(tasks["mind_tasks"]),
                "body_tasks_count": len(tasks["body_tasks"]),
                "tasks": tasks,
                "summary": f"You have {summary} in your {status} list.",
                "message": f"Found {summary}"
            }
            
        except Exception as e:
            logger.error("Error getting user tasks: %s", str(e))
            raise


class GetUserStatsTool(BaseTool):
    """Tool for retrieving user's statistics and progress"""
    
    @property
    def name(self) -> str:
        return "get_user_stats"
    
    @property
    def description(self) -> str:
        return """Get the user's statistics and progress information.
        
Use this tool when the user asks about:
- "How am I doing?"
- "Show me my progress"
- "What's my XP?"
- "How many tasks have I completed?"
- "What level am I?"
- Their achievements or overall performance

This provides insights into their productivity and wellness journey."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user"
                }
            },
            "required": ["user_id"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Get user's stats"""
        try:
            user_id = kwargs.get('user_id')
            
            # Get profile data
            profile = get_profile_by_user_id(user_id)
            
            # Get latest snapshot
            latest_snapshot = get_latest_snapshot(user_id)
            
            # Get stats summary (last 30 days)
            stats_summary = get_stats_summary(user_id, days=30)
            
            if not profile:
                return {
                    "success": False,
                    "message": "Could not retrieve your profile at this time."
                }
            
            logger.info("Retrieved stats for user %s", user_id)
            
            # Build comprehensive stats
            stats = {
                "level": profile.get('level', 1),
                "total_xp": profile.get('total_xp', 0),
                "current_streak": profile.get('current_streak', 0),
                "longest_streak": profile.get('longest_streak', 0),
                "tasks_completed": profile.get('tasks_completed_count', 0),
                "latest_snapshot": latest_snapshot,
                "performance_summary": stats_summary
            }
            
            return {
                "success": True,
                "stats": stats,
                "message": "Here are your current statistics and progress!"
            }
            
        except Exception as e:
            logger.error("Error getting user stats: %s", str(e))
            raise


# Example of how to create more query tools:
# 
# class GetAchievementsTool(BaseTool):
#     """Tool for getting user achievements"""
#     pass
# 
# class GetGoalsTool(BaseTool):
#     """Tool for getting user goals"""
#     pass
