# Ejemplos de Uso del Sistema de Tools

Este documento muestra ejemplos prácticos de cómo el agente usa las herramientas disponibles.

## Ejemplo 1: Crear una tarea mental

**Conversación del usuario:**
```
Usuario: Me siento estresado, ¿qué puedo hacer?
```

**El agente responde y crea la tarea:**
```
Agente: Te recomiendo hacer una sesión de meditación de 10 minutos. 
        La meditación puede ayudar a reducir el estrés y aclarar tu mente.
        ¿Quieres que la agregue a tus tareas?
        
Usuario: Sí, por favor

[El agente llama a create_mind_task]
{
  "user_id": "123",
  "title": "Meditación de 10 minutos",
  "description": "Toma 10 minutos para meditar. Encuentra un lugar tranquilo, siéntate cómodamente y enfócate en tu respiración. Deja que los pensamientos pasen sin juzgarlos.",
  "xp_reward": 20,
  "priority": "high",
  "estimated_duration": 10
}

Agente: ✅ ¡Listo! He agregado 'Meditación de 10 minutos' a tus tareas mentales. 
        Ganarás 20 XP cuando la completes.
```

## Ejemplo 2: Crear una tarea física

**Conversación del usuario:**
```
Usuario: Necesito hacer ejercicio pero no sé qué hacer
```

**El agente responde y crea la tarea:**
```
Agente: ¿Qué te parece una caminata de 30 minutos? Es un ejercicio excelente,
        de bajo impacto y puedes hacerlo al aire libre. ¿Te gustaría que la
        agregue a tu lista?
        
Usuario: Perfecto, agrégala

[El agente llama a create_body_task]
{
  "user_id": "123",
  "title": "Caminata de 30 minutos",
  "description": "Sal a caminar durante 30 minutos. Mantén un ritmo cómodo pero constante. Respira profundamente y disfruta del entorno. Puedes escuchar música o un podcast si lo deseas.",
  "xp_reward": 35,
  "priority": "medium",
  "estimated_duration": 30
}

Agente: ✅ He agregado 'Caminata de 30 minutos' a tus tareas físicas.
        Ganarás 35 XP al completarla. ¡Disfruta tu caminata!
```

## Ejemplo 3: Consultar tareas pendientes

**Conversación del usuario:**
```
Usuario: ¿Qué tareas tengo pendientes?
```

**El agente consulta y responde:**
```
[El agente llama a get_user_tasks]
{
  "user_id": "123",
  "task_type": "both",
  "status": "pending"
}

Respuesta: {
  "success": true,
  "mind_tasks_count": 2,
  "body_tasks_count": 1,
  "tasks": {
    "mind_tasks": [
      {
        "id": "m1",
        "title": "Leer 20 páginas",
        "xp_reward": 25
      },
      {
        "id": "m2",
        "title": "Meditación de 10 minutos",
        "xp_reward": 20
      }
    ],
    "body_tasks": [
      {
        "id": "b1",
        "title": "Caminata de 30 minutos",
        "xp_reward": 35
      }
    ]
  }
}

Agente: Tienes 3 tareas pendientes:
        
        📚 Tareas Mentales (2):
        1. Leer 20 páginas - 25 XP
        2. Meditación de 10 minutos - 20 XP
        
        💪 Tareas Físicas (1):
        1. Caminata de 30 minutos - 35 XP
        
        ¿En cuál te gustaría trabajar primero?
```

## Ejemplo 4: Completar una tarea

**Conversación del usuario:**
```
Usuario: Acabo de terminar la meditación
```

**El agente marca la tarea como completada:**
```
[El agente llama primero a get_user_tasks para encontrar la tarea de meditación]
[Luego llama a complete_task]
{
  "task_id": "m2",
  "task_type": "mind"
}

Respuesta: {
  "success": true,
  "task_id": "m2",
  "xp_awarded": 20,
  "message": "🎉 Congratulations! You completed 'Meditación de 10 minutos' and earned 20 XP!"
}

Agente: 🎉 ¡Excelente trabajo! Has completado la meditación y ganado 20 XP.
        ¿Cómo te sientes ahora?
```

## Ejemplo 5: Ver estadísticas

**Conversación del usuario:**
```
Usuario: ¿Cómo voy en mi progreso?
```

**El agente consulta las estadísticas:**
```
[El agente llama a get_user_stats]
{
  "user_id": "123"
}

Respuesta: {
  "success": true,
  "stats": {
    "total_xp": 450,
    "level": 5,
    "tasks_completed": 23,
    "current_streak": 7,
    "achievements": 12
  }
}

Agente: ¡Vas muy bien! 🌟
        
        📊 Tu progreso:
        - Nivel: 5
        - XP Total: 450
        - Tareas completadas: 23
        - Racha actual: 7 días
        - Logros desbloqueados: 12
        
        ¡Sigue así! Estás construyendo hábitos increíbles.
```

## Ejemplo 6: Flujo completo - Recomendación y creación múltiple

**Conversación del usuario:**
```
Usuario: Quiero ser más productivo mañana
```

**El agente hace recomendaciones y crea tareas:**
```
Agente: ¡Excelente iniciativa! Te recomiendo comenzar el día con una rutina
        que combine mente y cuerpo. ¿Qué te parece esto para mañana?
        
        🧠 Por la mañana:
        - 15 minutos de planificación del día
        - 20 minutos de lectura
        
        💪 Durante el día:
        - 30 minutos de ejercicio
        - Caminata después del almuerzo (15 min)
        
        ¿Quieres que agregue todas estas tareas?

Usuario: Sí, agrégalas todas

[El agente llama a create_mind_task múltiples veces]
[El agente llama a create_body_task múltiples veces]

Agente: ✅ ¡Perfecto! He agregado 4 tareas para mañana:
        
        📚 Tareas Mentales:
        1. Planificación diaria (15 min) - 20 XP
        2. Lectura matutina (20 min) - 25 XP
        
        💪 Tareas Físicas:
        1. Sesión de ejercicio (30 min) - 40 XP
        2. Caminata post-almuerzo (15 min) - 20 XP
        
        Total XP disponible: 105 puntos
        
        ¡Vas a tener un día increíble! 💪✨
```

## Ejemplo 7: Actualizar una tarea

**Conversación del usuario:**
```
Usuario: La tarea de "Leer 20 páginas" es muy ambiciosa, mejor solo 10 páginas
```

**El agente actualiza la tarea:**
```
[El agente llama a get_user_tasks para encontrar la tarea]
[Luego llama a update_task]
{
  "task_id": "m1",
  "task_type": "mind",
  "title": "Leer 10 páginas",
  "xp_reward": 15
}

Respuesta: {
  "success": true,
  "task_id": "m1",
  "updated_fields": ["title", "xp_reward"],
  "message": "✅ Task 'Leer 10 páginas' has been updated successfully!"
}

Agente: ✅ He actualizado tu tarea a "Leer 10 páginas" y ajustado el XP a 15 puntos.
        Es mejor empezar con metas alcanzables. ¡Puedes hacerlo! 📖
```

## Ejemplo 8: Contexto persistente

**El agente recuerda el contexto entre mensajes:**

```
Usuario: ¿Qué puedo hacer para dormir mejor?

Agente: Para mejorar tu sueño te recomiendo:
        - Meditación antes de dormir (10 min)
        - Evitar pantallas 1 hora antes
        - Mantener horarios regulares
        ¿Quieres que agregue la meditación nocturna a tus tareas?

Usuario: Sí

[Crea la tarea]

Usuario: ¿Y si también hago yoga?

Agente: ¡Excelente idea! El yoga complementa perfectamente la meditación.
        ¿Qué te parece una sesión de yoga relajante de 20 minutos antes
        de la meditación? Lo agrego a tus tareas físicas.

[Crea la tarea de yoga]

Usuario: Perfecto, ¿a qué hora debería hacerlas?

Agente: Te recomiendo:
        - 8:30 PM: Yoga relajante (20 min)
        - 9:00 PM: Meditación nocturna (10 min)
        - 9:30 PM: Prepararte para dormir
        
        Esto te permitirá estar en cama alrededor de las 10 PM,
        completamente relajado.
```

## Patrones de Interacción

### Patrón 1: Consultar antes de actuar
```
Usuario hace petición → Agente pregunta si desea crear → Usuario confirma → Agente crea
```

### Patrón 2: Acción directa (cuando es obvio)
```
Usuario dice "agrégala" → Agente crea inmediatamente
```

### Patrón 3: Consulta y recomendación
```
Usuario pregunta → Agente consulta datos → Agente da recomendación basada en datos
```

### Patrón 4: Múltiples acciones
```
Usuario pide varias cosas → Agente realiza múltiples llamadas a tools → Confirma todo
```

## Mejores Prácticas

1. **Siempre confirmar antes de crear tareas** (a menos que el usuario lo pida explícitamente)
2. **Usar get_user_tasks para obtener IDs** antes de completar o actualizar
3. **Proporcionar contexto y motivación** en las descripciones de tareas
4. **Ajustar XP según dificultad** (10-20: fácil, 30-50: medio, 60-100: difícil)
5. **Ser conversacional y natural**, no robótico
6. **Celebrar los logros** cuando se completan tareas
7. **Dar seguimiento** y preguntar cómo se sienten después de actividades
