"""
Script de ejemplo para probar los endpoints del backend.
Requiere tener el servidor corriendo en http://localhost:5000
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Imprime una respuesta HTTP de forma legible."""
    print(f"\n{'='*60}")
    print(f"📡 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def main():
    """Ejecuta pruebas de los endpoints principales."""
    
    # 1. LOGIN
    print("\n🔐 Iniciando pruebas del sistema...")
    
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print_response("LOGIN", response)
    
    if response.status_code != 200:
        print("\n❌ Error en login. Verifica tus credenciales.")
        print("💡 Asegúrate de tener un usuario en la base de datos.")
        return
    
    token = response.json().get('token')
    
    # Headers para requests autenticados
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 2. PERFIL
    print("\n\n👤 Probando endpoints de PERFIL...")
    
    # Obtener perfil (puede no existir todavía)
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    print_response("GET Profile", response)
    
    # Crear perfil si no existe
    if response.status_code == 404:
        profile_data = {
            "timezone": "America/Mexico_City",
            "birth_date": "1990-01-15",
            "gender": "male",
            "weight_kg": 75.5,
            "height_cm": 175,
            "preferred_language": "es"
        }
        response = requests.post(f"{BASE_URL}/api/profile", json=profile_data, headers=headers)
        print_response("CREATE Profile", response)
    
    # 3. PLANTILLAS DE TAREAS
    print("\n\n📋 Probando endpoints de PLANTILLAS...")
    
    response = requests.get(f"{BASE_URL}/api/task-templates", headers=headers)
    print_response("GET All Templates", response)
    
    # 4. TAREAS DE MENTE
    print("\n\n🧠 Probando endpoints de TAREAS DE MENTE...")
    
    response = requests.get(f"{BASE_URL}/api/tasks/mind", headers=headers)
    print_response("GET Mind Tasks", response)
    
    # 5. TAREAS DE CUERPO
    print("\n\n💪 Probando endpoints de TAREAS DE CUERPO...")
    
    response = requests.get(f"{BASE_URL}/api/tasks/body", headers=headers)
    print_response("GET Body Tasks", response)
    
    # 6. LOGROS
    print("\n\n🏆 Probando endpoints de LOGROS...")
    
    response = requests.get(f"{BASE_URL}/api/achievements", headers=headers)
    print_response("GET Achievements", response)
    
    # 7. METAS
    print("\n\n🎯 Probando endpoints de METAS...")
    
    response = requests.get(f"{BASE_URL}/api/goals", headers=headers)
    print_response("GET Goals", response)
    
    # Crear una meta de ejemplo
    goal_data = {
        "title": "Meditar 30 días seguidos",
        "description": "Completar una sesión de meditación cada día durante 30 días",
        "metric_key": "meditation_streak",
        "target_value": 30,
        "start_date": "2025-10-01",
        "end_date": "2025-10-31",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/api/goals", json=goal_data, headers=headers)
    print_response("CREATE Goal", response)
    
    # 8. CHAT IA
    print("\n\n💬 Probando endpoints de CHAT IA...")
    
    # Obtener sesiones
    response = requests.get(f"{BASE_URL}/api/chat/sessions", headers=headers)
    print_response("GET Chat Sessions", response)
    
    # Crear sesión
    session_data = {
        "title": "Consulta sobre meditación",
        "model": "gpt-5",
        "system_prompt": "Eres un asistente experto en mindfulness y meditación."
    }
    response = requests.post(f"{BASE_URL}/api/chat/sessions", json=session_data, headers=headers)
    print_response("CREATE Chat Session", response)
    
    if response.status_code == 201:
        session_id = response.json().get('id')
        
        # Crear mensaje
        message_data = {
            "role": "user",
            "content": "¿Cómo puedo mejorar mi práctica de meditación?"
        }
        response = requests.post(
            f"{BASE_URL}/api/chat/sessions/{session_id}/messages",
            json=message_data,
            headers=headers
        )
        print_response("CREATE Message", response)
        
        # Obtener mensajes
        response = requests.get(
            f"{BASE_URL}/api/chat/sessions/{session_id}/messages",
            headers=headers
        )
        print_response("GET Messages", response)
    
    # 9. TASK LOGS
    print("\n\n📝 Probando endpoints de TASK LOGS...")
    
    response = requests.get(f"{BASE_URL}/api/task-logs", headers=headers)
    print_response("GET Task Logs", response)
    
    # 10. FAILURES
    print("\n\n❌ Probando endpoints de FAILURES...")
    
    response = requests.get(f"{BASE_URL}/api/failures", headers=headers)
    print_response("GET Failures", response)
    
    # 11. BOT RULES
    print("\n\n🤖 Probando endpoints de BOT RULES...")
    
    response = requests.get(f"{BASE_URL}/api/bot-rules", headers=headers)
    print_response("GET Bot Rules", response)
    
    print("\n\n✅ Pruebas completadas!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se puede conectar al servidor.")
        print("💡 Asegúrate de que el servidor esté corriendo: python app.py")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
