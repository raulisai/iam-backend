"""
Script para probar el sistema de recomendaciones de tareas
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.task_recommendation_service import (
    get_recent_tasks,
    analyze_task_patterns,
    generate_recommendations_simple,
    generate_task_recommendations
)


def test_recommendations():
    """Test the recommendation system with mock data"""
    print("=" * 80)
    print("Testing Task Recommendation System")
    print("=" * 80)
    
    # This would normally use a real user_id from the database
    # For testing, you can use a UUID of an existing user
    test_user_id = "550e8400-e29b-41d4-a716-446655440000"  # Replace with real user ID
    
    try:
        print("\n1. Testing simple pattern-based recommendations...")
        print("-" * 80)
        
        result = generate_task_recommendations(test_user_id, use_ai=False)
        
        print(f"Method used: {result['method']}")
        print(f"Generated at: {result['generated_at']}")
        print(f"Task history count: {result['task_history_count']}")
        print(f"\nRecommendations ({len(result['recommendations'])}):")
        
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"\n  {i}. {rec['name']} ({rec['category']})")
            print(f"     Template ID: {rec['id']}")
            print(f"     Description: {rec.get('desc', 'N/A')}")
            print(f"     XP: {rec.get('default_xp', 0)}")
            print(f"     Suggested schedule: {rec.get('suggested_schedule', 'N/A')}")
            print(f"     Reason: {rec.get('reason', 'N/A')}")
        
        print("\n✓ Simple recommendations test completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error testing recommendations: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_with_ai():
    """Test AI-powered recommendations"""
    test_user_id = "550e8400-e29b-41d4-a716-446655440000"  # Replace with real user ID
    
    try:
        print("\n2. Testing AI-powered recommendations...")
        print("-" * 80)
        print("Note: This requires OpenAI API key and sufficient task history")
        
        result = generate_task_recommendations(test_user_id, use_ai=True)
        
        print(f"Method used: {result['method']}")
        print(f"Recommendations: {len(result['recommendations'])}")
        
        if result['method'] == 'ai_powered':
            print("\n✓ AI recommendations test completed successfully!")
        else:
            print("\n⚠ Fell back to pattern-based (expected if no API key or insufficient history)")
        
    except Exception as e:
        print(f"\n✗ Error testing AI recommendations: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    print("\n⚠ IMPORTANT: Update test_user_id with a valid user ID from your database\n")
    
    success = test_recommendations()
    
    if success:
        print("\n" + "=" * 80)
        print("Would you like to test AI recommendations? (requires API key)")
        response = input("Test AI? (y/n): ").strip().lower()
        
        if response == 'y':
            test_with_ai()
    
    print("\n" + "=" * 80)
    print("Testing completed!")
    print("=" * 80)
