# AI Agent Tools 🤖🔧

Esta carpeta contiene todas las herramientas (tools) disponibles para el agente de IA. Cada herramienta permite al agente realizar acciones específicas en el sistema.

## 📖 Documentación

| Documento | Descripción |
|-----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | 🚀 Inicio rápido (empieza aquí - 5 min) |
| **[README.md](README.md)** | 📚 Guía completa (este archivo) |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🏗️ Diagramas y arquitectura del sistema |
| **[DIAGRAMS.md](DIAGRAMS.md)** | 📊 Diagramas visuales de flujo |
| **[EXAMPLES.md](EXAMPLES.md)** | 💬 Ejemplos de conversaciones con el agente |
| **[TEMPLATE.py](TEMPLATE.py)** | 📝 Plantilla para crear nuevas tools |
| **[CHECKLIST.md](CHECKLIST.md)** | ✅ Checklist de verificación |

---

## Arquitectura

```
tools/
├── __init__.py              # Exports de todas las herramientas
├── base_tool.py             # Clase base (BaseTool, ToolRegistry)
├── task_tools.py            # Herramientas para crear tareas
├── query_tools.py           # Herramientas para consultar información
├── task_action_tools.py     # Herramientas para acciones en tareas
├── TEMPLATE.py              # Plantilla para crear nuevas herramientas
├── EXAMPLES.md              # Ejemplos de uso del sistema
└── README.md                # Esta documentación
```

### Componentes Principales

1. **BaseTool**: Clase abstracta que define la interfaz estándar
2. **ToolRegistry**: Sistema de registro que conecta tools con el agente
3. **Tool Modules**: Módulos específicos con implementaciones concretas
4. **Agent Service**: Servicio que inicializa y registra todas las tools

## Cómo Funciona

1. **BaseTool**: Clase abstracta que define la interfaz para todas las herramientas
2. **ToolRegistry**: Registro que gestiona y conecta las herramientas con el agente
3. **Herramientas específicas**: Implementaciones concretas que heredan de BaseTool

## Crear una Nueva Herramienta

### Paso 1: Crear la herramienta

Crea un nuevo archivo o añade a uno existente en la carpeta `tools/`:

```python
from typing import Dict, Any
from .base_tool import BaseTool

class MiNuevaHerramienta(BaseTool):
    """Descripción de tu herramienta"""
    
    @property
    def name(self) -> str:
        return "nombre_de_la_herramienta"
    
    @property
    def description(self) -> str:
        return """Descripción detallada de qué hace la herramienta.
        El agente usa esta descripción para decidir cuándo usarla."""
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Descripción del parámetro"
                },
                "param2": {
                    "type": "integer",
                    "description": "Otro parámetro"
                }
            },
            "required": ["param1"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Implementa la lógica de la herramienta"""
        param1 = kwargs.get('param1')
        param2 = kwargs.get('param2', 0)
        
        # Tu lógica aquí
        resultado = hacer_algo(param1, param2)
        
        return {
            "success": True,
            "result": resultado,
            "message": "Operación completada"
        }
    
    def validate_params(self, **kwargs) -> bool:
        """Validación opcional de parámetros"""
        param1 = kwargs.get('param1')
        return param1 is not None and len(param1) > 0
```

### Paso 2: Registrar en __init__.py

Agrega tu herramienta al archivo `tools/__init__.py`:

```python
from .mi_modulo import MiNuevaHerramienta

__all__ = [
    'BaseTool',
    'ToolRegistry',
    'CreateMindTaskTool',
    'CreateBodyTaskTool',
    'MiNuevaHerramienta',  # ← Agregar aquí
]
```

### Paso 3: Registrar en agent_service.py

Añade tu herramienta en el método `_register_tools`:

```python
def _register_tools(self):
    """Register all available tools"""
    from tools import MiNuevaHerramienta
    
    tools = [
        CreateMindTaskTool(),
        CreateBodyTaskTool(),
        MiNuevaHerramienta(),  # ← Agregar aquí
    ]
    
    self.tool_registry.register_tools(tools)
```

## Herramientas Disponibles

### CreateMindTaskTool
Crea tareas mentales/cognitivas para el usuario.

**Cuándo usarla**: Cuando el agente recomienda actividades mentales como lectura, meditación, planificación, etc.

**Parámetros**:
- `user_id` (required): ID del usuario
- `title` (required): Título de la tarea
- `description` (required): Descripción detallada
- `xp_reward` (required): Puntos XP (10-100)
- `priority` (optional): low/medium/high
- `estimated_duration` (optional): Duración estimada en minutos

### CreateBodyTaskTool
Crea tareas físicas/corporales para el usuario.

**Cuándo usarla**: Cuando el agente recomienda actividades físicas como ejercicio, yoga, caminata, etc.

**Parámetros**:
- `user_id` (required): ID del usuario
- `title` (required): Título de la tarea
- `description` (required): Descripción detallada
- `xp_reward` (required): Puntos XP (10-100)
- `priority` (optional): low/medium/high
- `estimated_duration` (optional): Duración estimada en minutos

## Ideas para Nuevas Herramientas

Aquí hay algunas ideas de herramientas que podrías implementar:

1. **GetUserTasksTool**: Consultar tareas pendientes del usuario
2. **UpdateTaskTool**: Modificar una tarea existente
3. **CompleteTaskTool**: Marcar una tarea como completada
4. **CreateGoalTool**: Crear objetivos a largo plazo
5. **GetUserStatsTool**: Obtener estadísticas del usuario
6. **GetAchievementsTool**: Consultar logros del usuario
7. **AddFailureTool**: Registrar un fallo/aprendizaje
8. **SearchTaskTemplatesTool**: Buscar plantillas de tareas
9. **SetReminderTool**: Configurar recordatorios
10. **GenerateReportTool**: Generar informes de progreso

## Mejores Prácticas

1. **Nombres descriptivos**: Usa nombres claros que indiquen la acción
2. **Descripciones detalladas**: El agente usa esto para decidir cuándo usar la tool
3. **Validación**: Valida parámetros antes de ejecutar
4. **Manejo de errores**: Usa try/except y retorna información útil
5. **Logging**: Registra acciones importantes para debugging
6. **Mensajes al usuario**: Retorna mensajes claros sobre qué se hizo
7. **Atomicidad**: Cada tool debe hacer una cosa y hacerla bien
8. **Documentación**: Documenta los parámetros y comportamiento esperado

## Esquema de Respuesta

Todas las herramientas deben retornar un diccionario con esta estructura mínima:

```python
{
    "success": True/False,      # Indica si la operación fue exitosa
    "message": "...",            # Mensaje para el usuario
    # ... otros campos específicos de la herramienta
}
```

En caso de error, la estructura debe incluir:

```python
{
    "success": False,
    "error": "descripción del error",
    "tool": "nombre_de_la_herramienta"
}
```

## Testing

Para probar una herramienta:

```python
from tools import MiNuevaHerramienta

tool = MiNuevaHerramienta()
result = tool.execute(param1="test", param2=123)
print(result)
```

## Depuración

Si una herramienta no funciona:

1. Verifica que está registrada en `__init__.py`
2. Verifica que está añadida en `_register_tools` en agent_service.py
3. Revisa los logs del servidor para ver errores
4. Verifica que los parámetros coinciden con el schema JSON
5. Asegúrate que la validación no está rechazando los parámetros
