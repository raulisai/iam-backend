"""Agent service for AI interactions with extensible tool system."""
import logging
from typing import Optional
from lib.agent import AIAgent
from tools import ToolRegistry, CreateMindTaskTool, CreateBodyTaskTool

logger = logging.getLogger(__name__)


class AgentService:
    """Service for managing AI agent interactions with dynamic tool loading"""
    
    def __init__(self):
        """Initialize the AI agent with a system prompt and register tools"""
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

🔧 YOU HAVE POWERFUL TOOLS:
You can CREATE tasks directly for users when you recommend them:

WORKFLOW FOR CREATING TASKS:
1. First, use get_task_templates to see available templates (if you haven't already)
2. Choose an appropriate template_key from the results
3. Use create_mind_task or create_body_task with that template_key

- Use create_mind_task for mental/cognitive tasks (reading, learning, meditation, planning, etc.)
- Use create_body_task for physical tasks (exercise, yoga, walking, sports, etc.)

IMPORTANT: Tasks are created from TEMPLATES. You MUST provide a template_key when creating tasks.
The template_key is a string identifier (e.g., 'meditation_15', 'daily_reading_01', 'morning_run_01').

When you suggest a task, you can IMMEDIATELY create it if the user agrees.
Example conversation flow:
User: "I feel stressed"
You: "I recommend a 10-minute breathing meditation. Would you like me to add this to your tasks?"
User: "Yes, please"
You: *uses get_task_templates to find 'meditation_15' or similar*
You: *creates task using create_mind_task with template_key='meditation_15', params={'duration': 10}*
You: "Done! I've added '10-minute meditation' to your mind tasks."

Guidelines:
- Be natural, warm, and conversational
- Answer questions directly and concisely
- Match the user's language and tone
- Don't repeat yourself or use template responses
- If asked about the date or time, provide helpful information
- Be supportive but also practical
- Keep responses focused and relevant to what the user asks
- Always use template_key (not template_id) when creating tasks
- Get templates first to see available template_keys
- Customize tasks using the params object (e.g., {'duration': 30, 'notes': 'morning session'})"""
        
        self.agent = AIAgent(
            name="WellnessProductivityAssistant",
            model="gpt-4-turbo-preview",
            temperature=0.7,
            system_prompt=system_prompt
        )
        
        # Initialize tool registry and register all tools
        self.tool_registry = ToolRegistry(self.agent)
        self._register_tools()
        
        logger.info("Agent service initialized with %d tools", len(self.tool_registry.list_tools()))
    
    def _register_tools(self):
        """
        Register all available tools with the agent
        Add new tools here to make them available to the agent
        """
        from tools import GetUserTasksTool, GetUserStatsTool, GetTaskTemplatesTool
        
        tools = [
            # Template query tools - IMPORTANT: Agent should use this first to find template IDs
            GetTaskTemplatesTool(),
            
            # Task creation tools
            CreateMindTaskTool(),
            CreateBodyTaskTool(),
            
            # Query tools
            GetUserTasksTool(),
            GetUserStatsTool(),
            
            # Add more tools here as you create them:
            # CompleteTaskTool(),
            # CreateGoalTool(),
            # UpdateProfileTool(),
            # etc.
        ]
        
        self.tool_registry.register_tools(tools)
        logger.info("Registered tools: %s", ', '.join(self.tool_registry.list_tools()))
    
    def get_available_tools(self):
        """Get information about all available tools"""
        return self.tool_registry.get_tool_info()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Global service instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """Get or create agent service instance"""
    global _agent_service  # noqa: PLW0603
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
