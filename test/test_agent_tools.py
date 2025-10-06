"""
Test script for the agent tools system
Run this to verify that tools are registered and working correctly
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.agent_service import get_agent_service
from lib.agent import AIAgent


def test_tool_registration():
    """Test that all tools are registered correctly"""
    print("=" * 60)
    print("Testing Tool Registration")
    print("=" * 60)
    
    try:
        # Get the agent service
        agent_service = get_agent_service()
        
        # Get tool info
        tools = agent_service.get_available_tools()
        
        print(f"\n✅ Successfully loaded agent service")
        print(f"✅ Total tools registered: {len(tools)}\n")
        
        # Display each tool
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {tool['name']}")
            print(f"   Description: {tool['description'][:80]}...")
            required_params = tool['parameters'].get('properties', {}).keys()
            print(f"   Parameters: {', '.join(required_params)}")
            print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_tool_execution():
    """Test actual tool execution (simulation)"""
    print("=" * 60)
    print("Testing Tool Execution (Simulation)")
    print("=" * 60)
    
    try:
        # Get the agent service
        agent_service = get_agent_service()
        agent = agent_service.agent
        
        # Test 1: List available functions
        print("\n📋 Available functions:")
        functions = agent.list_available_functions()
        for func in functions:
            print(f"   - {func}")
        
        # Test 2: Try to execute a function directly (simulation)
        print("\n🧪 Testing direct function execution...")
        
        # Test create_mind_task
        print("\n1. Testing create_mind_task:")
        result = agent.execute_function(
            "create_mind_task",
            {
                "user_id": "test-user-123",
                "title": "Test meditation task",
                "description": "This is a test task created by the testing script",
                "xp_reward": 20,
                "priority": "medium",
                "estimated_duration": 10
            }
        )
        print(f"   Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_conversation():
    """Test agent conversation with tools"""
    print("\n" + "=" * 60)
    print("Testing Agent Conversation with Tools")
    print("=" * 60)
    
    try:
        # Get the agent service
        agent_service = get_agent_service()
        agent = agent_service.agent
        
        # Test conversation
        test_user_id = "test-user-123"
        
        print(f"\n🤖 Starting conversation with agent...")
        print(f"User ID: {test_user_id}\n")
        
        # Example 1: Ask for task recommendations
        prompt = "I'm feeling stressed. Can you help me?"
        print(f"User: {prompt}")
        
        response = await agent.ask(
            prompt,
            conversation_id="test-session",
            user_context={"user_id": test_user_id}
        )
        
        print(f"\nAgent: {response['content']}")
        print(f"\nFunction calls made: {response.get('function_calls_made', 0)}")
        
        if response.get('function_results'):
            print("\nFunction results:")
            for result in response['function_results']:
                print(f"   - {result}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def print_summary():
    """Print summary and usage instructions"""
    print("\n" + "=" * 60)
    print("Tool System Summary")
    print("=" * 60)
    
    print("""
The tool system is set up with the following architecture:

📁 tools/
   ├── __init__.py           - Exports all tools
   ├── base_tool.py          - Base classes (BaseTool, ToolRegistry)
   ├── task_tools.py         - Task creation tools
   ├── query_tools.py        - Query/retrieval tools
   ├── task_action_tools.py  - Task action tools (complete, update)
   ├── TEMPLATE.py           - Template for new tools
   ├── README.md             - Documentation
   └── EXAMPLES.md           - Usage examples

🔧 Available Tool Categories:
   1. Task Creation:
      - create_mind_task
      - create_body_task
   
   2. Task Queries:
      - get_user_tasks
      - get_user_stats
   
   3. Task Actions:
      - complete_task (in task_action_tools.py, needs registration)
      - update_task (in task_action_tools.py, needs registration)

📝 To Add a New Tool:
   1. Create tool class inheriting from BaseTool
   2. Add to tools/__init__.py
   3. Register in services/agent_service.py _register_tools()
   4. Test with this script!

🚀 The agent can now:
   ✅ Create mind and body tasks for users
   ✅ Retrieve user's task lists
   ✅ Get user statistics
   ✅ Respond in the user's language
   ✅ Make intelligent decisions about when to use tools
   ✅ Handle multi-turn conversations with context

🎯 Next Steps:
   - Add more tools as needed (goals, achievements, etc.)
   - Test with real users
   - Monitor agent decisions and tool usage
   - Refine tool descriptions for better agent understanding
""")


def main():
    """Run all tests"""
    print("\n🧪 Agent Tools System Test Suite\n")
    
    # Test 1: Registration
    success1 = test_tool_registration()
    
    # Test 2: Execution (only if registration worked)
    success2 = False
    if success1:
        success2 = asyncio.run(test_tool_execution())
    
    # Test 3: Conversation (optional, requires API key)
    # Uncomment to test full conversation:
    # success3 = asyncio.run(test_agent_conversation())
    
    # Print summary
    print_summary()
    
    # Final result
    print("\n" + "=" * 60)
    if success1 and success2:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
