"""
Test script para verificar el funcionamiento del sistema de goal_tasks.
Este script prueba todos los endpoints principales.

NOTA: Asegúrate de tener un usuario creado y obtener su token JWT primero.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:5000"
TOKEN = "YOUR_JWT_TOKEN_HERE"  # Reemplazar con un token válido

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def print_response(response, title="Response"):
    """Helper para imprimir respuestas formateadas."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_goal_tasks_workflow():
    """Test completo del flujo de goal_tasks."""
    
    print("\n🎯 INICIANDO TEST DE GOAL TASKS SYSTEM")
    
    # 1. Crear un goal
    print("\n\n📌 PASO 1: Crear un Goal")
    goal_data = {
        "title": "Meditar 30 días seguidos",
        "description": "Goal de meditación para octubre",
        "target_value": 30,
        "metric_key": "meditation_days",
        "start_date": "2025-10-01",
        "end_date": "2025-10-31",
        "is_active": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/goals/",
        headers=headers,
        json=goal_data
    )
    print_response(response, "1. Goal creado")
    
    if response.status_code != 201:
        print("❌ Error creando goal. Abortando test.")
        return
    
    goal_id = response.json()["id"]
    print(f"\n✅ Goal creado con ID: {goal_id}")
    
    # 2. Crear una tarea recurrente
    print("\n\n📌 PASO 2: Crear tarea recurrente diaria")
    task_data = {
        "title": "Meditación matutina",
        "description": "Sesión de meditación de 10 minutos",
        "type": "mind",
        "required": True,
        "weight": 1,
        "schedule_rrule": "FREQ=DAILY;BYHOUR=8;BYMINUTE=0"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/goals/{goal_id}/tasks",
        headers=headers,
        json=task_data
    )
    print_response(response, "2. Tarea creada")
    
    if response.status_code != 201:
        print("❌ Error creando tarea. Abortando test.")
        return
    
    task_id = response.json()["id"]
    print(f"\n✅ Tarea creada con ID: {task_id}")
    
    # 3. Generar ocurrencias para el mes
    print("\n\n📌 PASO 3: Generar ocurrencias")
    generate_data = {
        "start_date": "2025-10-01T00:00:00Z",
        "end_date": "2025-10-31T23:59:59Z"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/goals/tasks/{task_id}/occurrences/generate",
        headers=headers,
        json=generate_data
    )
    print_response(response, "3. Ocurrencias generadas")
    
    if response.status_code != 201:
        print("❌ Error generando ocurrencias. Abortando test.")
        return
    
    occurrences_count = response.json()["generated"]
    occurrences = response.json()["occurrences"]
    print(f"\n✅ {occurrences_count} ocurrencias generadas")
    
    # 4. Listar ocurrencias
    print("\n\n📌 PASO 4: Listar ocurrencias con status")
    response = requests.get(
        f"{BASE_URL}/api/goals/tasks/{task_id}/occurrences?include_status=true",
        headers=headers
    )
    print_response(response, "4. Lista de ocurrencias")
    
    if not occurrences:
        print("⚠️ No hay ocurrencias para continuar el test")
        return
    
    occurrence_id = occurrences[0]["id"]
    
    # 5. Marcar primera ocurrencia como completada
    print("\n\n📌 PASO 5: Marcar ocurrencia como completada")
    log_data = {
        "action": "completed",
        "metadata": {
            "value": 1,
            "notes": "Excelente sesión de meditación"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/goals/occurrences/{occurrence_id}/log",
        headers=headers,
        json=log_data
    )
    print_response(response, "5. Log creado")
    
    # 6. Ver progreso del goal
    print("\n\n📌 PASO 6: Ver progreso del goal")
    response = requests.get(
        f"{BASE_URL}/api/goals/{goal_id}/progress",
        headers=headers
    )
    print_response(response, "6. Progreso del goal")
    
    progress = response.json()["progress_percent"]
    print(f"\n✅ Progreso actual: {progress}% (1/30 = {1/30*100:.2f}%)")
    
    # 7. Marcar más ocurrencias como completadas
    print("\n\n📌 PASO 7: Completar 4 ocurrencias más")
    for i in range(1, min(5, len(occurrences))):
        occ_id = occurrences[i]["id"]
        log_data = {
            "action": "completed",
            "metadata": {"value": 1}
        }
        response = requests.post(
            f"{BASE_URL}/api/goals/occurrences/{occ_id}/log",
            headers=headers,
            json=log_data
        )
        print(f"  ✓ Ocurrencia {i+1} completada: {response.status_code}")
    
    # 8. Ver progreso actualizado
    print("\n\n📌 PASO 8: Ver progreso actualizado")
    response = requests.get(
        f"{BASE_URL}/api/goals/{goal_id}/progress",
        headers=headers
    )
    print_response(response, "8. Progreso actualizado")
    
    progress = response.json()["progress_percent"]
    print(f"\n✅ Progreso actualizado: {progress}% (5/30 = {5/30*100:.2f}%)")
    
    # 9. Ver logs de una ocurrencia
    print("\n\n📌 PASO 9: Ver logs de la primera ocurrencia")
    response = requests.get(
        f"{BASE_URL}/api/goals/occurrences/{occurrence_id}/logs",
        headers=headers
    )
    print_response(response, "9. Logs de la ocurrencia")
    
    # 10. Obtener detalles de una ocurrencia
    print("\n\n📌 PASO 10: Obtener detalles de ocurrencia con status")
    response = requests.get(
        f"{BASE_URL}/api/goals/occurrences/{occurrence_id}",
        headers=headers
    )
    print_response(response, "10. Detalles de la ocurrencia")
    
    # 11. Listar todas las tareas del goal
    print("\n\n📌 PASO 11: Listar todas las tareas del goal")
    response = requests.get(
        f"{BASE_URL}/api/goals/{goal_id}/tasks",
        headers=headers
    )
    print_response(response, "11. Lista de tareas")
    
    # 12. Actualizar tarea
    print("\n\n📌 PASO 12: Actualizar tarea")
    update_data = {
        "title": "Meditación matutina (15 minutos)",
        "weight": 1.5
    }
    response = requests.put(
        f"{BASE_URL}/api/goals/tasks/{task_id}",
        headers=headers,
        json=update_data
    )
    print_response(response, "12. Tarea actualizada")
    
    print("\n\n" + "="*60)
    print("✅ TEST COMPLETADO EXITOSAMENTE")
    print("="*60)
    print(f"\nResumen:")
    print(f"  - Goal ID: {goal_id}")
    print(f"  - Task ID: {task_id}")
    print(f"  - Ocurrencias generadas: {occurrences_count}")
    print(f"  - Ocurrencias completadas: 5")
    print(f"  - Progreso final: {progress}%")
    print("\n💡 Puedes ver el goal en: GET /api/goals/{goal_id}")
    print(f"💡 Swagger docs: {BASE_URL}/apidocs")


def test_one_time_task():
    """Test de tarea puntual (no recurrente)."""
    
    print("\n\n🎯 TEST DE TAREA PUNTUAL")
    
    # Crear goal
    goal_data = {
        "title": "Comprar equipo de ejercicio",
        "description": "Goal para comprar equipo",
        "target_value": 1,
        "metric_key": "equipment_purchased",
        "start_date": "2025-10-01",
        "is_active": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/goals/",
        headers=headers,
        json=goal_data
    )
    print_response(response, "Goal para tarea puntual")
    
    if response.status_code != 201:
        return
    
    goal_id = response.json()["id"]
    
    # Crear tarea puntual
    task_data = {
        "title": "Comprar colchoneta de yoga",
        "description": "Colchoneta acolchada para yoga",
        "type": "one_off",
        "required": True,
        "weight": 1,
        "due_at": "2025-10-15T12:00:00Z"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/goals/{goal_id}/tasks",
        headers=headers,
        json=task_data
    )
    print_response(response, "Tarea puntual creada")
    
    if response.status_code != 201:
        return
    
    task_id = response.json()["id"]
    
    # Generar ocurrencia (solo una)
    response = requests.post(
        f"{BASE_URL}/api/goals/tasks/{task_id}/occurrences/generate",
        headers=headers,
        json={"start_date": "2025-10-01T00:00:00Z", "end_date": "2025-10-31T23:59:59Z"}
    )
    print_response(response, "Ocurrencia generada")
    
    print("\n✅ Test de tarea puntual completado")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║        GOAL TASKS SYSTEM - TEST SCRIPT                   ║
╚══════════════════════════════════════════════════════════╝

IMPORTANTE: 
1. Asegúrate de que el servidor esté corriendo en localhost:5000
2. Reemplaza TOKEN con un JWT válido de un usuario autenticado
3. El usuario debe existir en la base de datos

Presiona Enter para continuar o Ctrl+C para cancelar...
    """)
    
    input()
    
    if TOKEN == "YOUR_JWT_TOKEN_HERE":
        print("\n❌ ERROR: Debes reemplazar TOKEN con un JWT válido")
        print("   1. Crea un usuario con POST /api/auth/register")
        print("   2. Inicia sesión con POST /api/auth/login")
        print("   3. Copia el token del response")
        print("   4. Reemplaza TOKEN en este script\n")
        exit(1)
    
    try:
        # Test principal: flujo completo de tareas recurrentes
        test_goal_tasks_workflow()
        
        # Test adicional: tarea puntual
        # test_one_time_task()
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
