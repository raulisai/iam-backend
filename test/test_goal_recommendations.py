"""
Example script to test Goal Task Recommendations API
Demonstrates how to get AI-powered task recommendations for a goal
"""
import requests
import json
import os
from datetime import datetime

# Configuration
BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
API_URL = f"{BASE_URL}/api"

# You need to have a valid JWT token
# You can get this by logging in first
TOKEN = os.getenv('JWT_TOKEN', 'your-jwt-token-here')


def login(email, password):
    """Login to get JWT token."""
    url = f"{API_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        return result.get('token')
    else:
        print(f"Login failed: {response.text}")
        return None


def create_test_goal(token, title, description, end_date=None):
    """Create a test goal."""
    url = f"{API_URL}/goals"
    
    if not end_date:
        from datetime import datetime, timedelta
        start = datetime.now()
        end_date = (start + timedelta(days=180)).strftime('%Y-%m-%d')
        start_date = start.strftime('%Y-%m-%d')
    else:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    data = {
        "title": title,
        "description": description,
        "start_date": start_date,
        "end_date": end_date,
        "target_value": 100,
        "is_active": True
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Goal creation failed: {response.text}")
        return None


def get_goal_recommendations_simple(goal_id, token, count=5, use_ai=True):
    """Get simple task recommendations for a goal."""
    url = f"{API_URL}/goals/{goal_id}/recommendations"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'use_ai': str(use_ai).lower(),
        'count': count
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_goal_recommendations_with_context(goal_id, token, context, count=5):
    """Get task recommendations with additional context."""
    url = f"{API_URL}/goals/{goal_id}/recommendations"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'use_ai': 'true',
        'count': count
    }
    
    data = {
        'context': context
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()


def display_recommendations(result):
    """Display recommendations in a nice format."""
    if not result.get('success', True):
        print(f"\n❌ Error: {result.get('error')}")
        return
    
    print("\n" + "="*80)
    print(f"🎯 RECOMENDACIONES PARA: {result['goal']['title']}")
    print(f"📝 {result['goal']['description']}")
    print(f"📊 Método: {result['method']}")
    print(f"📅 Generado: {result['generated_at']}")
    print(f"📋 Tareas existentes: {result['existing_task_count']}")
    
    if result.get('ai_metadata'):
        print(f"🤖 Tokens usados: {result['ai_metadata']['tokens_used']}")
        print(f"🔮 Modelo: {result['ai_metadata']['model']}")
    
    print("="*80)
    
    recommendations = result.get('recommendations', [])
    
    if not recommendations:
        print("\n⚠️ No se generaron recomendaciones")
        return
    
    print(f"\n📌 {len(recommendations)} TAREAS RECOMENDADAS:\n")
    
    for i, rec in enumerate(recommendations, 1):
        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(rec.get('priority', 'medium').lower(), '⚪')
        
        print(f"{i}. {rec['title']}")
        print(f"   {priority_emoji} Prioridad: {rec.get('priority', 'N/A').upper()}")
        if rec.get('estimated_duration'):
            print(f"   ⏱️  Duración: {rec['estimated_duration']}")
        print(f"   📖 {rec['description']}")
        if rec.get('reason'):
            print(f"   💡 Razón: {rec['reason']}")
        if rec.get('template_id'):
            print(f"   🎨 Template ID: {rec['template_id']}")
        print()


def create_goal_task_from_recommendation(goal_id, token, recommendation):
    """Create a goal task from a recommendation."""
    url = f"{API_URL}/goals/{goal_id}/tasks"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "title": recommendation['title'],
        "description": recommendation['description'],
        "priority": recommendation.get('priority', 'medium'),
        "template_id": recommendation.get('template_id')
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()


# =============================================================================
# EXAMPLES
# =============================================================================

def example_1_simple_recommendations():
    """Example 1: Simple recommendations without context."""
    print("\n" + "="*80)
    print("EJEMPLO 1: Recomendaciones Simples")
    print("="*80)
    
    # First login
    email = input("Email: ") if TOKEN == 'your-jwt-token-here' else "test@example.com"
    password = input("Password: ") if TOKEN == 'your-jwt-token-here' else "test123"
    
    token = login(email, password) if TOKEN == 'your-jwt-token-here' else TOKEN
    
    if not token:
        print("❌ Could not authenticate")
        return
    
    # Create a test goal
    print("\n📝 Creando objetivo de prueba...")
    goal = create_test_goal(
        token,
        "Aprender Python Avanzado",
        "Dominar conceptos avanzados de Python incluyendo async, decoradores, metaclases y testing"
    )
    
    if not goal:
        print("❌ Could not create goal")
        return
    
    goal_id = goal.get('id')
    print(f"✅ Goal creado: {goal_id}")
    
    # Get recommendations
    print("\n🤖 Obteniendo recomendaciones con IA...")
    result = get_goal_recommendations_simple(goal_id, token, count=5, use_ai=True)
    
    display_recommendations(result)


def example_2_recommendations_with_context():
    """Example 2: Recommendations with additional context."""
    print("\n" + "="*80)
    print("EJEMPLO 2: Recomendaciones con Contexto Adicional")
    print("="*80)
    
    # Assume we have token and goal_id from previous example
    token = TOKEN
    goal_id = input("\nIngresa Goal ID: ")
    
    # Define context
    context = {
        "current_challenges": "Tengo poco tiempo libre, solo 1 hora diaria en las mañanas",
        "available_time": "1 hora por día, de 6:00 AM a 7:00 AM",
        "resources": [
            "Laptop personal",
            "Curso Udemy Python avanzado (ya adquirido)",
            "Libro 'Fluent Python'",
            "Acceso a ChatGPT"
        ],
        "preferences": "Prefiero tareas prácticas de 30-60 minutos, enfoque en proyectos reales"
    }
    
    print("\n📋 Contexto proporcionado:")
    print(json.dumps(context, indent=2, ensure_ascii=False))
    
    # Get recommendations with context
    print("\n🤖 Obteniendo recomendaciones personalizadas...")
    result = get_goal_recommendations_with_context(goal_id, token, context, count=3)
    
    display_recommendations(result)


def example_3_full_workflow():
    """Example 3: Complete workflow from goal creation to task creation."""
    print("\n" + "="*80)
    print("EJEMPLO 3: Flujo Completo - Goal → Recomendaciones → Tareas")
    print("="*80)
    
    token = TOKEN
    
    # Step 1: Create goal
    print("\n[PASO 1] Creando objetivo...")
    goal = create_test_goal(
        token,
        "Crear Mi Primera App Web",
        "Desarrollar y desplegar una aplicación web completa con backend y frontend"
    )
    
    if not goal:
        return
    
    goal_id = goal['id']
    print(f"✅ Goal creado: {goal['title']} (ID: {goal_id})")
    
    # Step 2: Get recommendations with context
    print("\n[PASO 2] Obteniendo recomendaciones...")
    context = {
        "current_challenges": "Soy principiante en desarrollo web",
        "available_time": "2-3 horas diarias después del trabajo",
        "resources": ["Laptop", "Internet", "GitHub account"],
        "preferences": "Quiero aprender haciendo, paso a paso con proyecto real"
    }
    
    result = get_goal_recommendations_with_context(goal_id, token, context, count=5)
    
    if not result.get('success', True):
        print(f"❌ Error: {result.get('error')}")
        return
    
    display_recommendations(result)
    
    # Step 3: Let user select which recommendations to create as tasks
    print("\n[PASO 3] Crear tareas desde recomendaciones")
    print("¿Qué recomendaciones quieres convertir en tareas?")
    
    recommendations = result['recommendations']
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']}")
    
    selections = input("\nIngresa números separados por comas (ej: 1,2,3) o 'all': ").strip()
    
    if selections.lower() == 'all':
        selected_indices = list(range(len(recommendations)))
    else:
        selected_indices = [int(x.strip()) - 1 for x in selections.split(',') if x.strip().isdigit()]
    
    print(f"\n📝 Creando {len(selected_indices)} tareas...")
    
    for idx in selected_indices:
        if 0 <= idx < len(recommendations):
            rec = recommendations[idx]
            print(f"\nCreando: {rec['title']}")
            task = create_goal_task_from_recommendation(goal_id, token, rec)
            if task:
                print(f"  ✅ Tarea creada con ID: {task.get('id')}")
            else:
                print(f"  ❌ Error al crear tarea")
    
    print("\n🎉 ¡Proceso completo!")
    print(f"\nPuedes ver tus tareas en: {API_URL}/goals/{goal_id}/tasks")


def example_4_compare_ai_vs_simple():
    """Example 4: Compare AI vs simple recommendations."""
    print("\n" + "="*80)
    print("EJEMPLO 4: Comparación AI vs Lógica Simple")
    print("="*80)
    
    token = TOKEN
    goal_id = input("\nIngresa Goal ID: ")
    
    # Get AI recommendations
    print("\n🤖 RECOMENDACIONES CON IA:")
    print("-" * 80)
    result_ai = get_goal_recommendations_simple(goal_id, token, count=3, use_ai=True)
    display_recommendations(result_ai)
    
    # Get simple recommendations
    print("\n📊 RECOMENDACIONES CON LÓGICA SIMPLE:")
    print("-" * 80)
    result_simple = get_goal_recommendations_simple(goal_id, token, count=3, use_ai=False)
    display_recommendations(result_simple)
    
    print("\n💡 ANÁLISIS:")
    print("- AI tiende a dar recomendaciones más específicas y contextualizadas")
    print("- Lógica simple da recomendaciones genéricas pero útiles")
    print("- AI consume tokens de OpenAI, simple es gratis")


# =============================================================================
# MAIN MENU
# =============================================================================

def main():
    """Main menu to select examples."""
    print("\n" + "="*80)
    print("🎯 GOAL TASK RECOMMENDATIONS - EJEMPLOS DE USO")
    print("="*80)
    
    while True:
        print("\nSelecciona un ejemplo:")
        print("1. Recomendaciones simples")
        print("2. Recomendaciones con contexto adicional")
        print("3. Flujo completo (crear goal, recomendaciones, tareas)")
        print("4. Comparar AI vs lógica simple")
        print("0. Salir")
        
        choice = input("\nOpción: ").strip()
        
        if choice == '1':
            example_1_simple_recommendations()
        elif choice == '2':
            example_2_recommendations_with_context()
        elif choice == '3':
            example_3_full_workflow()
        elif choice == '4':
            example_4_compare_ai_vs_simple()
        elif choice == '0':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida")


if __name__ == "__main__":
    # Check if TOKEN is set
    if TOKEN == 'your-jwt-token-here':
        print("\n⚠️  WARNING: No JWT_TOKEN environment variable set")
        print("You'll need to provide credentials to login\n")
    
    main()
