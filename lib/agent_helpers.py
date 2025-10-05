"""
Internal Agent Utilities - Helper functions to use AI agents within existing endpoints
These functions are NOT exposed as public endpoints but used internally by controllers
"""

import logging
from typing import Dict, Any, Optional, List
from services.agent_service import get_agent_service

logger = logging.getLogger(__name__)


class AgentHelper:
    """Helper class to use agents internally in controllers"""
    
    def __init__(self):
        self.service = get_agent_service()
    
    async def analyze_task_priority(self, task_title: str, task_description: str) -> str:
        """
        Use AI to suggest task priority based on title and description
        
        Args:
            task_title: Task title
            task_description: Task description
            
        Returns:
            Suggested priority: 'low', 'medium', or 'high'
        """
        try:
            prompt = f"""Analyze this task and suggest a priority level (low, medium, or high).
            
Task: {task_title}
Description: {task_description}

Consider:
- Urgency keywords (urgent, asap, immediately)
- Impact keywords (critical, important, minor)
- Deadlines mentioned
- Context clues

Respond with ONLY one word: low, medium, or high"""
            
            result = await self.service.agent.ask(
                prompt,
                conversation_id="priority_analyzer",
                user_context={"task": task_title}
            )
            
            if result.get("success"):
                response = result["response"].strip().lower()
                if response in ["low", "medium", "high"]:
                    return response
            
            return "medium"  # Default fallback
            
        except Exception as e:
            logger.error(f"Error analyzing task priority: {str(e)}")
            return "medium"
    
    async def suggest_task_category(self, task_title: str, task_description: str) -> str:
        """
        Use AI to suggest task category
        
        Args:
            task_title: Task title
            task_description: Task description
            
        Returns:
            Suggested category
        """
        try:
            prompt = f"""Categorize this task. Choose the most appropriate category.
            
Task: {task_title}
Description: {task_description}

Common categories: work, personal, health, learning, shopping, errands, social, finance

Respond with ONLY the category name."""
            
            result = await self.service.agent.ask(
                prompt,
                conversation_id="category_analyzer"
            )
            
            if result.get("success"):
                return result["response"].strip().lower()
            
            return "personal"
            
        except Exception as e:
            logger.error(f"Error suggesting category: {str(e)}")
            return "personal"
    
    async def generate_task_suggestions(self, user_id: int, goal_title: str) -> List[Dict]:
        """
        Generate task suggestions based on a goal
        
        Args:
            user_id: User ID
            goal_title: Goal title
            
        Returns:
            List of suggested tasks
        """
        try:
            prompt = f"""Generate 3-5 actionable tasks to achieve this goal: "{goal_title}"

For each task, provide:
1. A clear, concise title
2. A brief description
3. Estimated time (format: "30m", "1h", "2h")

Format your response as a simple numbered list."""
            
            result = await self.service.agent.ask(
                prompt,
                conversation_id=f"goal_planner_{user_id}",
                user_context={"user_id": user_id, "goal": goal_title}
            )
            
            if result.get("success"):
                # Parse the response into task suggestions
                # This is a simplified version - you could make it more robust
                return {
                    "suggestions": result["response"],
                    "goal": goal_title
                }
            
            return {"suggestions": [], "goal": goal_title}
            
        except Exception as e:
            logger.error(f"Error generating task suggestions: {str(e)}")
            return {"suggestions": [], "error": str(e)}
    
    async def analyze_task_completion_patterns(self, user_id: int) -> Dict[str, Any]:
        """
        Analyze user's task completion patterns using the agent
        
        Args:
            user_id: User ID
            
        Returns:
            Analysis with insights and recommendations
        """
        try:
            prompt = f"""Analyze the task statistics for user {user_id} and provide insights.
            
Use the get_task_statistics function to get the data, then provide:
1. Key patterns observed
2. Productivity insights
3. Recommendations for improvement

Keep it concise and actionable."""
            
            result = await self.service.agent.ask(
                prompt,
                conversation_id=f"analytics_{user_id}",
                user_context={"user_id": user_id}
            )
            
            return {
                "success": result.get("success", False),
                "analysis": result.get("response", ""),
                "function_calls": result.get("function_calls", [])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing patterns: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def smart_task_update(self, task_id: int, natural_language_update: str, user_id: int) -> Dict:
        """
        Update a task using natural language
        
        Args:
            task_id: Task ID
            natural_language_update: Natural language description of update
            user_id: User ID making the update
            
        Returns:
            Update result
        """
        try:
            prompt = f"""Update task {task_id} based on this instruction: "{natural_language_update}"
            
Use the appropriate function to update the task. If the instruction mentions:
- "done", "finished", "completed" -> set status to "completed"
- "working on", "started", "in progress" -> set status to "in_progress"
- "later", "postpone", "not now" -> set status to "pending"

Then confirm what was updated."""
            
            result = await self.service.agent.ask(
                prompt,
                conversation_id=f"task_updater_{user_id}",
                user_context={"user_id": user_id, "task_id": task_id}
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in smart task update: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def generate_achievement_description(self, achievement_type: str, count: int) -> str:
        """
        Generate a motivational achievement description
        
        Args:
            achievement_type: Type of achievement (e.g., "tasks_completed")
            count: Number achieved
            
        Returns:
            Motivational description
        """
        try:
            prompt = f"""Create a short, motivational description for an achievement.
            
Achievement: {achievement_type}
Count: {count}

Make it encouraging and celebratory. Maximum 100 characters.
Respond with ONLY the description text."""
            
            result = await self.service.agent.ask(
                prompt,
                conversation_id="achievement_generator"
            )
            
            if result.get("success"):
                return result["response"].strip()
            
            return f"Completed {count} {achievement_type}!"
            
        except Exception as e:
            logger.error(f"Error generating achievement: {str(e)}")
            return f"Achievement unlocked!"
    
    async def validate_and_enhance_profile(self, profile_data: Dict) -> Dict[str, Any]:
        """
        Validate profile data and suggest enhancements
        
        Args:
            profile_data: User profile data
            
        Returns:
            Validation result with suggestions
        """
        try:
            prompt = f"""Review this user profile and provide suggestions for improvement:

Profile: {profile_data}

Provide:
1. Is the profile complete? (yes/no)
2. What's missing or could be improved?
3. Brief suggestions (max 3)

Keep it concise."""
            
            result = await self.service.agent.ask(
                prompt,
                conversation_id="profile_validator"
            )
            
            return {
                "valid": True,  # You could parse the response for actual validation
                "suggestions": result.get("response", ""),
                "profile": profile_data
            }
            
        except Exception as e:
            logger.error(f"Error validating profile: {str(e)}")
            return {"valid": True, "suggestions": "", "profile": profile_data}


# Global helper instance
_agent_helper: Optional[AgentHelper] = None


def get_agent_helper() -> AgentHelper:
    """Get or create agent helper instance"""
    global _agent_helper
    if _agent_helper is None:
        _agent_helper = AgentHelper()
    return _agent_helper


# Convenience functions for quick use in controllers

async def ai_suggest_priority(title: str, description: str = "") -> str:
    """Quick function to get AI-suggested priority"""
    helper = get_agent_helper()
    return await helper.analyze_task_priority(title, description)


async def ai_suggest_category(title: str, description: str = "") -> str:
    """Quick function to get AI-suggested category"""
    helper = get_agent_helper()
    return await helper.suggest_task_category(title, description)


async def ai_analyze_user(user_id: int) -> Dict:
    """Quick function to analyze user patterns"""
    helper = get_agent_helper()
    return await helper.analyze_task_completion_patterns(user_id)


async def ai_generate_tasks_for_goal(user_id: int, goal: str) -> Dict:
    """Quick function to generate task suggestions for a goal"""
    helper = get_agent_helper()
    return await helper.generate_task_suggestions(user_id, goal)
