"""
Script de prueba para el sistema de Chat en Tiempo Real
Ejecutar con: python test_chat_realtime.py
"""

import requests
import json
import time

# Configuración
API_BASE_URL = "http://localhost:5000/api"
EMAIL = "test@example.com"  # Cambia esto
PASSWORD = "password123"     # Cambia esto

def print_section(title):
    """Imprime un título de sección."""
    print("\n" + "="*50)
    print(f"  {title}")
    print("="*50 + "\n")


# Timeout para requests HTTP (30 segundos)
REQUEST_TIMEOUT = 30

def login():
    """Realiza login y obtiene el token."""
    print_section("1. LOGIN")
    
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        print("✅ Login exitoso!")
        print(f"Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(response.json())
        return None

def create_session(token):
    """Crea una sesión de chat."""
    print_section("2. CREAR SESIÓN DE CHAT")
    
    response = requests.post(
        f"{API_BASE_URL}/chat/realtime/sessions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "title": "Test Session - Python Script",
            "initial_message": "Hola, este es un test"
        },
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code == 201:
        data = response.json()
        session_id = data.get("id")
        print("✅ Sesión creada exitosamente!")
        print(f"Session ID: {session_id}")
        print(f"Título: {data.get('title')}")
        return session_id
    else:
        print(f"❌ Error creando sesión: {response.status_code}")
        print(response.json())
        return None

def send_streaming_message(token, session_id, message):
    """Envía un mensaje y recibe respuesta en streaming."""
    print_section("3. ENVIAR MENSAJE CON STREAMING")
    
    print(f"📤 Enviando: '{message}'")
    print("📥 Respuesta en tiempo real:")
    print("-" * 50)
    
    response = requests.post(
        f"{API_BASE_URL}/chat/realtime/sessions/{session_id}/stream",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={"content": message},
        stream=True,  # Importante para streaming
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code == 200:
        full_content = ""
        
        # Leer el stream
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                
                # Procesar eventos SSE
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        
                        if data['type'] == 'start':
                            print("🚀 Iniciando stream...\n")
                        
                        elif data['type'] == 'content':
                            content = data['content']
                            full_content += content
                            print(content, end='', flush=True)
                        
                        elif data['type'] == 'done':
                            print("\n\n✅ Stream completado!")
                            print(f"Message ID: {data.get('message_id')}")
                        
                        elif data['type'] == 'error':
                            print(f"\n❌ Error: {data.get('error')}")
                    
                    except json.JSONDecodeError as e:
                        print(f"\n⚠️  Error parseando JSON: {e}")
        
        print("-" * 50)
        return True
    else:
        print(f"❌ Error enviando mensaje: {response.status_code}")
        print(response.text)
        return False

def main():
    """Función principal del test."""
    print("\n🧪 INICIANDO PRUEBAS DEL CHAT EN TIEMPO REAL")
    print("=" * 50)
    
    # 1. Login
    token = login()
    if not token:
        print("\n❌ No se pudo obtener el token. Verifica credenciales.")
        return
    
    time.sleep(1)
    
    # 2. Crear sesión
    session_id = create_session(token)
    if not session_id:
        print("\n❌ No se pudo crear la sesión.")
        return
    
    time.sleep(1)
    
    # 3. Enviar mensajes de prueba
    test_messages = [
        "¿Cómo puedo mejorar mi productividad?",
        "Dame 3 consejos cortos sobre meditación",
        "Explica la importancia del descanso"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*50}")
        print(f"  MENSAJE {i}/{len(test_messages)}")
        print('='*50)
        
        success = send_streaming_message(token, session_id, message)
        
        if not success:
            print(f"\n❌ Error en mensaje {i}")
            break
        
        # Esperar un poco entre mensajes
        if i < len(test_messages):
            print("\n⏳ Esperando 3 segundos antes del siguiente mensaje...")
            time.sleep(3)
    
    print("\n" + "="*50)
    print("  ✅ PRUEBAS COMPLETADAS")
    print("="*50)
    print(f"\nSession ID para revisar: {session_id}")
    print("Puedes ver los mensajes en la demo HTML o en Supabase")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
    except (OSError, ValueError, KeyError) as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
