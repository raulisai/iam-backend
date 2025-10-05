"""
Script rápido para probar el chat con diferentes tipos de mensajes
"""
import asyncio
from services.agent_service import get_agent_service

async def test_agent_responses():
    """Prueba rápida del agente con diferentes tipos de mensajes"""
    
    agent_service = get_agent_service()
    
    test_messages = [
        ("hi", "Test 1: Saludo simple en inglés"),
        ("helpe me", "Test 2: Petición de ayuda (con typo)"),
        ("que dia es hoy?", "Test 3: Pregunta en español"),
        ("¿Cómo puedo ser más productivo?", "Test 4: Pregunta sobre productividad"),
        ("I need to organize my tasks", "Test 5: Necesidad en inglés"),
    ]
    
    print("=" * 80)
    print("PRUEBA DE RESPUESTAS DEL AGENTE")
    print("=" * 80)
    
    for i, (message, description) in enumerate(test_messages, 1):
        print(f"\n{description}")
        print("-" * 80)
        print(f"👤 Usuario: {message}")
        
        try:
            result = await agent_service.agent.ask(
                message,
                conversation_id=f"test_conv_{i}",
                user_context={"test": True}
            )
            
            if result.get("success"):
                response = result.get('response', 'No response')
                print(f"🤖 Coach AI: {response}")
            else:
                print(f"❌ Error: {result.get('error')}")
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("=" * 80)
    print("PRUEBA COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_agent_responses())
