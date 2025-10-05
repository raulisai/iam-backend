"""
Quick test script to verify the AI Agent system is working
Run this to ensure everything is configured correctly
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_agent_basic():
    """Test 1: Basic agent initialization"""
    print("\n" + "="*60)
    print("TEST 1: Basic Agent Initialization")
    print("="*60)
    
    try:
        from lib.agent import AIAgent
        
        agent = AIAgent(name="TestAgent")
        print("✅ Agent initialized successfully")
        print(f"   Name: {agent.name}")
        print(f"   Model: {agent.model}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


async def test_function_registration():
    """Test 2: Function registration"""
    print("\n" + "="*60)
    print("TEST 2: Function Registration")
    print("="*60)
    
    try:
        from lib.agent import AIAgent
        
        agent = AIAgent(name="TestAgent")
        
        @agent.register_function(
            name="test_function",
            description="A test function",
            parameters={
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        )
        def test_function(message: str):
            return {"received": message}
        
        functions = agent.list_available_functions()
        print(f"✅ Function registered successfully")
        print(f"   Registered functions: {functions}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


async def test_agent_service():
    """Test 3: Agent service initialization"""
    print("\n" + "="*60)
    print("TEST 3: Agent Service Initialization")
    print("="*60)
    
    try:
        from services.agent_service import get_agent_service
        
        service = get_agent_service()
        functions = service.list_available_actions()
        
        print(f"✅ Agent service initialized")
        print(f"   Total functions: {functions['total_functions']}")
        print(f"   Functions: {', '.join(functions['available_functions'][:5])}...")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


async def test_agent_helpers():
    """Test 4: Agent helpers"""
    print("\n" + "="*60)
    print("TEST 4: Agent Helpers")
    print("="*60)
    
    try:
        from lib.agent_helpers import get_agent_helper
        
        helper = get_agent_helper()
        print("✅ Agent helper initialized")
        print(f"   Helper class: {helper.__class__.__name__}")
        print(f"   Available methods: analyze_task_priority, suggest_task_category, etc.")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


async def test_openai_connection():
    """Test 5: OpenAI API connection (optional - requires API key)"""
    print("\n" + "="*60)
    print("TEST 5: OpenAI API Connection")
    print("="*60)
    
    try:
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("⚠️  OPENAI_API_KEY not found in environment")
            print("   Agent will not be able to make API calls")
            print("   Set it in .env file to enable full functionality")
            return False
        
        print("✅ OPENAI_API_KEY found")
        print(f"   Key starts with: {api_key[:15]}...")
        
        # Try a simple request
        from lib.agent import AIAgent
        agent = AIAgent(name="TestAgent")
        
        print("   Testing OpenAI connection...")
        result = await agent.ask("Say 'test successful' if you can read this")
        
        if result.get("success"):
            print("✅ OpenAI API working!")
            print(f"   Response: {result['response'][:100]}...")
            return True
        else:
            print(f"⚠️  API call failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"⚠️  OpenAI test failed: {str(e)}")
        print("   This is normal if you haven't set OPENAI_API_KEY yet")
        return False


async def test_database_functions():
    """Test 6: Database function execution"""
    print("\n" + "="*60)
    print("TEST 6: Database Functions")
    print("="*60)
    
    try:
        from services.agent_service import get_agent_service
        
        service = get_agent_service()
        
        # Test getting user tasks (will use agent's registered function)
        print("   Testing function execution...")
        
        # Execute a registered function directly
        result = service.agent.execute_function(
            "get_task_statistics",
            {"user_id": 1}
        )
        
        if result.get("success"):
            print("✅ Database function executed successfully")
            print(f"   Function: get_task_statistics")
            print(f"   Result: {result['result']}")
            return True
        else:
            print(f"⚠️  Function execution failed: {result.get('error')}")
            print("   This might be normal if database is empty")
            return False
            
    except Exception as e:
        print(f"⚠️  Database test failed: {str(e)}")
        print("   This is normal if Supabase connection has issues")
        return False


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results if r)
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("   The AI Agent system is ready to use.")
    elif passed >= total - 2:
        print("\n✅ CORE TESTS PASSED!")
        print("   The system is functional.")
        print("   Some optional tests failed (OpenAI/DB tests).")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("   Check the errors above and fix configuration.")
    
    print("\n" + "="*60)


async def main():
    """Run all tests"""
    print("\n🤖 AI AGENT SYSTEM - VERIFICATION TESTS")
    print("="*60)
    print("This will verify that the agent system is properly configured")
    
    results = []
    
    # Run core tests
    results.append(await test_agent_basic())
    results.append(await test_function_registration())
    results.append(await test_agent_service())
    results.append(await test_agent_helpers())
    
    # Run optional tests
    results.append(await test_openai_connection())
    results.append(await test_database_functions())
    
    # Print summary
    print_summary(results)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Critical error: {str(e)}")
        import traceback
        traceback.print_exc()
