"""
Ejemplo de cómo probar el Chat IA con el agente integrado
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:5000/api"
TOKEN = "TU_TOKEN_JWT_AQUI"  # Reemplaza con un token válido

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def test_chat_flow():
    """Prueba completa del flujo de chat con respuestas del agente"""
    
    print("=" * 60)
    print("Prueba de Chat IA con Agente")
    print("=" * 60)
    
    # 1. Crear una nueva sesión de chat
    print("\n1. Creando nueva sesión de chat...")
    session_data = {
        "title": "Conversación sobre productividad"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/sessions",
        headers=headers,
        json=session_data
    )
    
    if response.status_code != 201:
        print(f"Error creando sesión: {response.text}")
        return
    
    session = response.json()
    session_id = session['id']
    print(f"✓ Sesión creada: {session_id}")
    print(f"  Título: {session.get('title')}")
    
    # 2. Enviar primer mensaje del usuario
    print("\n2. Enviando mensaje del usuario...")
    message_data = {
        "role": "user",
        "content": "Hola! Necesito ayuda para organizar mis tareas del día. ¿Qué me recomiendas?"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/sessions/{session_id}/messages",
        headers=headers,
        json=message_data
    )
    
    if response.status_code != 201:
        print(f"Error enviando mensaje: {response.text}")
        return
    
    result = response.json()
    print(f"✓ Mensaje enviado")
    print(f"\n  Usuario dijo: {result['user_message']['content']}")
    
    if 'assistant_message' in result:
        print(f"\n  🤖 Asistente respondió:")
        print(f"  {result['assistant_message']['content']}")
    else:
        print("\n  ⚠️ No se generó respuesta del asistente")
    
    # 3. Enviar segundo mensaje
    print("\n3. Enviando segundo mensaje...")
    message_data = {
        "role": "user",
        "content": "Genial! ¿Y qué técnicas de productividad me recomiendas para empezar?"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/sessions/{session_id}/messages",
        headers=headers,
        json=message_data
    )
    
    if response.status_code != 201:
        print(f"Error enviando mensaje: {response.text}")
        return
    
    result = response.json()
    print(f"✓ Segundo mensaje enviado")
    print(f"\n  Usuario dijo: {result['user_message']['content']}")
    
    if 'assistant_message' in result:
        print(f"\n  🤖 Asistente respondió:")
        print(f"  {result['assistant_message']['content']}")
    
    # 4. Obtener todos los mensajes de la sesión
    print("\n4. Obteniendo historial completo...")
    response = requests.get(
        f"{BASE_URL}/chat/sessions/{session_id}/messages",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Error obteniendo mensajes: {response.text}")
        return
    
    messages = response.json()
    print(f"✓ Total de mensajes: {len(messages)}")
    
    print("\n📝 Historial completo:")
    print("-" * 60)
    for i, msg in enumerate(messages, 1):
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        emoji = "👤" if role == "user" else "🤖"
        print(f"{i}. {emoji} {role.upper()}: {content[:100]}{'...' if len(content) > 100 else ''}")
    
    # 5. Obtener información de la sesión
    print("\n5. Obteniendo información de la sesión...")
    response = requests.get(
        f"{BASE_URL}/chat/sessions/{session_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        session_info = response.json()
        print(f"✓ Sesión actualizada:")
        print(f"  Título: {session_info.get('title')}")
        print(f"  Último mensaje: {session_info.get('last_message_at')}")
    
    print("\n" + "=" * 60)
    print("✓ Prueba completada exitosamente!")
    print("=" * 60)
    
    return session_id


def test_single_message(session_id=None, message="Hola, ¿cómo puedes ayudarme?"):
    """Prueba rápida enviando un solo mensaje"""
    
    # Crear sesión si no existe
    if not session_id:
        response = requests.post(
            f"{BASE_URL}/chat/sessions",
            headers=headers,
            json={"title": "Prueba rápida"}
        )
        session_id = response.json()['id']
    
    # Enviar mensaje
    message_data = {
        "role": "user",
        "content": message
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/sessions/{session_id}/messages",
        headers=headers,
        json=message_data
    )
    
    if response.status_code == 201:
        result = response.json()
        print(f"\n👤 TÚ: {message}")
        if 'assistant_message' in result:
            print(f"🤖 ASISTENTE: {result['assistant_message']['content']}")
        return result
    else:
        print(f"Error: {response.text}")
        return None


if __name__ == "__main__":
    # Asegúrate de tener un token válido antes de ejecutar
    if TOKEN == "TU_TOKEN_JWT_AQUI":
        print("⚠️  ERROR: Necesitas configurar un TOKEN válido")
        print("\nPara obtener un token:")
        print("1. Registra un usuario en POST /api/auth/register")
        print("2. O inicia sesión en POST /api/auth/login")
        print("3. Copia el token de la respuesta")
        print("4. Actualiza la variable TOKEN en este archivo")
    else:
        try:
            test_chat_flow()
            
            # Prueba adicional
            print("\n\n¿Quieres hacer otra pregunta? (opcional)")
            # test_single_message(message="¿Cómo puedo mejorar mi concentración?")
            
        except requests.exceptions.ConnectionError:
            print("⚠️  ERROR: No se puede conectar al servidor")
            print("Asegúrate de que el servidor Flask esté corriendo en http://localhost:5000")
        except Exception as e:
            print(f"⚠️  ERROR: {str(e)}")
