"""
Robust AI Agent Service with OpenAI Integration and MCP Support
Handles intelligent actions, function calling, and multi-agent orchestration
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from functools import wraps

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Custom exception for agent-related errors"""
    pass


class FunctionRegistry:
    """Registry to manage available functions for agent execution"""
    
    def __init__(self):
        self._functions: Dict[str, Callable] = {}
        self._schemas: Dict[str, Dict] = {}
    
    def register(self, name: str, description: str, parameters: Dict[str, Any]):
        """
        Decorator to register a function for agent use
        
        Args:
            name: Function name
            description: Function description for the agent
            parameters: JSON schema for function parameters
        """
        def decorator(func: Callable):
            self._functions[name] = func
            self._schemas[name] = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters
                }
            }
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_function(self, name: str) -> Optional[Callable]:
        """Get a registered function by name"""
        return self._functions.get(name)
    
    def get_schemas(self) -> List[Dict]:
        """Get all function schemas for OpenAI"""
        return list(self._schemas.values())
    
    def list_functions(self) -> List[str]:
        """List all registered function names"""
        return list(self._functions.keys())


class AgentConversation:
    """Manages conversation history and context"""
    
    def __init__(self, system_prompt: str, max_history: int = 50):
        self.messages: List[Dict[str, str]] = []
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.utcnow().isoformat(),
            "total_tokens": 0,
            "function_calls": 0
        }
        
        # Add system message
        self.add_message("system", system_prompt)
    
    def add_message(self, role: str, content: str, tool_calls: Optional[List] = None):
        """Add a message to conversation history"""
        message = {"role": role, "content": content}
        if tool_calls:
            message["tool_calls"] = tool_calls
        
        self.messages.append(message)
        
        # Trim history if needed
        if len(self.messages) > self.max_history:
            # Keep system message and trim oldest messages
            self.messages = [self.messages[0]] + self.messages[-(self.max_history-1):]
    
    def add_tool_message(self, tool_call_id: str, content: str):
        """Add a tool/function response message"""
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content
        })
    
    def get_messages(self) -> List[Dict]:
        """Get all conversation messages"""
        return self.messages
    
    def clear(self):
        """Clear conversation history except system prompt"""
        system_msg = self.messages[0] if self.messages else None
        self.messages = [system_msg] if system_msg else []


class AIAgent:
    """
    Robust AI Agent with OpenAI integration and MCP support
    Handles function calling, multi-turn conversations, and intelligent action execution
    """
    
    def __init__(
        self,
        name: str = "DefaultAgent",
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        system_prompt: Optional[str] = None
    ):
        """
        Initialize AI Agent
        
        Args:
            name: Agent identifier
            model: OpenAI model to use
            temperature: Response randomness (0-2)
            max_tokens: Maximum tokens in response
            system_prompt: System instructions for the agent
        """
        self.name = name
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AgentError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        
        # Function registry
        self.function_registry = FunctionRegistry()
        
        # Default system prompt
        default_prompt = f"""You are {name}, an intelligent AI assistant that helps execute actions and provide information.
You have access to various functions that you can call to perform specific tasks.
Always be helpful, accurate, and efficient in your responses.
When calling functions, ensure you have all required parameters."""
        
        self.system_prompt = system_prompt or default_prompt
        
        # Active conversations (supports multiple concurrent conversations)
        self.conversations: Dict[str, AgentConversation] = {}
        
        # Agent statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens_used": 0,
            "total_function_calls": 0
        }
        
        logger.info(f"Agent '{name}' initialized with model '{model}'")
    
    def register_function(self, name: str, description: str, parameters: Dict[str, Any]):
        """
        Register a function that the agent can call
        
        Args:
            name: Function name
            description: What the function does
            parameters: JSON schema for parameters
            
        Example:
            @agent.register_function(
                name="create_task",
                description="Creates a new task for a user",
                parameters={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Task title"},
                        "user_id": {"type": "integer", "description": "User ID"}
                    },
                    "required": ["title", "user_id"]
                }
            )
            def create_task(title: str, user_id: int):
                # Implementation
                pass
        """
        return self.function_registry.register(name, description, parameters)
    
    def get_or_create_conversation(self, conversation_id: str) -> AgentConversation:
        """Get existing conversation or create new one"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = AgentConversation(self.system_prompt)
        return self.conversations[conversation_id]
    
    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered function
        
        Args:
            function_name: Name of function to execute
            arguments: Function arguments
            
        Returns:
            Dict with success status and result or error
        """
        try:
            func = self.function_registry.get_function(function_name)
            if not func:
                return {
                    "success": False,
                    "error": f"Function '{function_name}' not found"
                }
            
            logger.info(f"Executing function: {function_name} with args: {arguments}")
            result = func(**arguments)
            
            self.stats["total_function_calls"] += 1
            
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            logger.error(f"Error executing function '{function_name}': {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_tool_calls(self, tool_calls: List) -> List[Dict]:
        """Process multiple tool calls from the agent"""
        results = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute the function
            result = self.execute_function(function_name, function_args)
            
            results.append({
                "tool_call_id": tool_call.id,
                "function_name": function_name,
                "result": result
            })
        
        return results
    
    async def ask(
        self,
        prompt: str,
        conversation_id: str = "default",
        user_context: Optional[Dict[str, Any]] = None,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Send a prompt to the agent and get response with function execution
        
        Args:
            prompt: User prompt/question
            conversation_id: Conversation identifier for context
            user_context: Additional context (user_id, metadata, etc.)
            max_iterations: Maximum function call iterations
            
        Returns:
            Dict containing response, function calls, and metadata
        """
        self.stats["total_requests"] += 1
        
        try:
            conversation = self.get_or_create_conversation(conversation_id)
            
            # Add user context to prompt if provided
            if user_context:
                enhanced_prompt = f"{prompt}\n\nContext: {json.dumps(user_context)}"
            else:
                enhanced_prompt = prompt
            
            conversation.add_message("user", enhanced_prompt)
            
            # Iterative function calling
            iteration = 0
            function_call_history = []
            
            while iteration < max_iterations:
                iteration += 1
                
                # Create completion
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation.get_messages(),
                    tools=self.function_registry.get_schemas() if self.function_registry.get_schemas() else None,
                    tool_choice="auto" if self.function_registry.get_schemas() else None,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                message = response.choices[0].message
                
                # Update stats
                if hasattr(response, 'usage'):
                    self.stats["total_tokens_used"] += response.usage.total_tokens
                    conversation.metadata["total_tokens"] += response.usage.total_tokens
                
                # Check if agent wants to call functions
                if message.tool_calls:
                    conversation.add_message(
                        "assistant",
                        message.content or "",
                        tool_calls=[tc.model_dump() for tc in message.tool_calls]
                    )
                    
                    # Process all tool calls
                    tool_results = self.process_tool_calls(message.tool_calls)
                    function_call_history.extend(tool_results)
                    
                    # Add tool responses to conversation
                    for tool_result in tool_results:
                        conversation.add_tool_message(
                            tool_result["tool_call_id"],
                            json.dumps(tool_result["result"])
                        )
                    
                    # Continue loop to let agent process results
                    continue
                else:
                    # No more function calls, we have final response
                    conversation.add_message("assistant", message.content or "")
                    
                    self.stats["successful_requests"] += 1
                    
                    return {
                        "success": True,
                        "response": message.content,
                        "function_calls": function_call_history,
                        "conversation_id": conversation_id,
                        "iterations": iteration,
                        "metadata": {
                            "model": self.model,
                            "tokens_used": conversation.metadata["total_tokens"],
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    }
            
            # Max iterations reached
            logger.warning(f"Max iterations ({max_iterations}) reached for conversation {conversation_id}")
            return {
                "success": False,
                "error": "Maximum function call iterations reached",
                "response": "I encountered too many function calls. Please try rephrasing your request.",
                "function_calls": function_call_history
            }
            
        except OpenAIError as e:
            self.stats["failed_requests"] += 1
            logger.error(f"OpenAI API error: {str(e)}")
            return {
                "success": False,
                "error": f"OpenAI API error: {str(e)}"
            }
        except Exception as e:
            self.stats["failed_requests"] += 1
            logger.error(f"Unexpected error in agent.ask: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def clear_conversation(self, conversation_id: str = "default"):
        """Clear a specific conversation history"""
        if conversation_id in self.conversations:
            self.conversations[conversation_id].clear()
            logger.info(f"Cleared conversation: {conversation_id}")
    
    def delete_conversation(self, conversation_id: str):
        """Delete a conversation entirely"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Deleted conversation: {conversation_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent usage statistics"""
        return {
            **self.stats,
            "active_conversations": len(self.conversations),
            "registered_functions": len(self.function_registry.list_functions())
        }
    
    def list_available_functions(self) -> List[str]:
        """List all available functions"""
        return self.function_registry.list_functions()


class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents for complex tasks
    Useful for task delegation and parallel processing
    """
    
    def __init__(self):
        self.agents: Dict[str, AIAgent] = {}
        logger.info("MultiAgentOrchestrator initialized")
    
    def add_agent(self, agent: AIAgent):
        """Add an agent to the orchestrator"""
        self.agents[agent.name] = agent
        logger.info(f"Agent '{agent.name}' added to orchestrator")
    
    def get_agent(self, name: str) -> Optional[AIAgent]:
        """Get an agent by name"""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())
    
    async def delegate_task(
        self,
        agent_name: str,
        prompt: str,
        conversation_id: Optional[str] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Delegate a task to a specific agent
        
        Args:
            agent_name: Name of the agent to use
            prompt: Task prompt
            conversation_id: Optional conversation ID
            user_context: Optional user context
            
        Returns:
            Agent response
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return {
                "success": False,
                "error": f"Agent '{agent_name}' not found"
            }
        
        conversation_id = conversation_id or f"{agent_name}_default"
        return await agent.ask(prompt, conversation_id, user_context)
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics from all agents"""
        return {
            agent_name: agent.get_stats()
            for agent_name, agent in self.agents.items()
        }


# Global agent instance (singleton pattern)
_default_agent: Optional[AIAgent] = None


def get_default_agent() -> AIAgent:
    """Get or create the default agent instance"""
    global _default_agent
    if _default_agent is None:
        _default_agent = AIAgent(
            name="IAMAssistant",
            model="gpt-4-turbo-preview",
            system_prompt="""You are IAM Assistant, an intelligent agent that helps manage tasks, 
            goals, profiles, and other features in the IAM Backend system.
            You have access to various database operations and can help users accomplish their goals efficiently.
            Always be helpful, precise, and secure in your operations."""
        )
    return _default_agent


# Convenience function for quick agent usage
async def ask_agent(prompt: str, conversation_id: str = "default", user_context: Optional[Dict] = None) -> Dict:
    """Quick function to ask the default agent"""
    agent = get_default_agent()
    return await agent.ask(prompt, conversation_id, user_context)
