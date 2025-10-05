"""Agent service for AI interactions."""
import logging
from typing import Optional
from lib.agent import AIAgent

logger = logging.getLogger(__name__)


class AgentService:
    """Service for managing AI agent interactions"""
    
    def __init__(self):
        """Initialize the AI agent with a system prompt for the chat"""
        system_prompt = """You are Coach AI, a helpful and friendly AI assistant for a productivity and wellness application.

IMPORTANT: Always respond in the SAME LANGUAGE that the user writes to you. If they write in Spanish, respond in Spanish. If they write in English, respond in English.

Your role is to help users with:
- Task management and productivity tips
- Wellness and mindfulness guidance  
- Goal setting and achievement strategies
- Time management and prioritization
- Encouragement and motivation
- Stress management techniques
- Building healthy habits
- General questions and conversation

Guidelines:
- Be natural, warm, and conversational
- Answer questions directly and concisely
- Match the user's language and tone
- Don't repeat yourself or use template responses
- If asked about the date or time, provide helpful information
- Be supportive but also practical
- Keep responses focused and relevant to what the user asks"""
        
        self.agent = AIAgent(
            name="WellnessProductivityAssistant",
            model="gpt-4-turbo-preview",
            temperature=0.7,
            system_prompt=system_prompt
        )
        logger.info("Agent service initialized")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Global service instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """Get or create agent service instance"""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
