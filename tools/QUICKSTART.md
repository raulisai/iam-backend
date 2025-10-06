# 🚀 Guía Rápida - Sistema de Tools del Agente

## ¿Qué es esto?

Un sistema extensible que permite al agente de IA realizar **acciones automáticas** como crear tareas, consultar información, completar actividades, etc.

## 🎯 Inicio Rápido (5 minutos)

### 1. Verificar que está funcionando

```bash
# En el directorio del proyecto
python test/test_agent_tools.py
```

Si ves ✅ "All tests passed!", todo está funcionando.

### 2. Probar con el chat

Inicia el servidor y prueba estos mensajes:

```
Usuario: "Me siento estresado, ¿qué puedo hacer?"
Agente: [Recomienda meditación] "¿Quieres que la agregue a tus tareas?"
Usuario: "Sí, por favor"
Agente: ✅ [Crea la tarea automáticamente]
```

### 3. Ver las tools disponibles

```python
from services.agent_service import get_agent_service

agent_service = get_agent_service()
tools = agent_service.get_available_tools()

for tool in tools:
    print(f"- {tool['name']}")
```

## 📦 Tools Incluidas

| Tool | Descripción | Cuándo se usa |
|------|-------------|---------------|
| `create_mind_task` | Crea tareas mentales | El usuario acepta una recomendación de lectura, meditación, etc. |
| `create_body_task` | Crea tareas físicas | El usuario acepta una recomendación de ejercicio, yoga, etc. |
| `get_user_tasks` | Consulta tareas del usuario | El usuario pregunta "¿qué tareas tengo?" |
| `get_user_stats` | Obtiene estadísticas | El usuario pregunta "¿cómo voy?" |

## ➕ Agregar una Nueva Tool (3 pasos)

### Paso 1: Crear la tool

```python
# tools/my_tools.py
from tools.base_tool import BaseTool
from typing import Dict, Any

class MyNewTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_action"
    
    @property
    def description(self) -> str:
        return "Description of what this tool does"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "param1": {"type": "string"}
            },
            "required": ["user_id", "param1"]
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        user_id = kwargs.get('user_id')
        param1 = kwargs.get('param1')
        
        # Tu lógica aquí
        result = do_something(user_id, param1)
        
        return {
            "success": True,
            "message": "Done!",
            "result": result
        }
```

### Paso 2: Exportar en __init__.py

```python
# tools/__init__.py
from .my_tools import MyNewTool

__all__ = [
    # ... existing tools
    'MyNewTool',
]
```

### Paso 3: Registrar en agent_service.py

```python
# services/agent_service.py
def _register_tools(self):
    from tools import MyNewTool
    
    tools = [
        # ... existing tools
        MyNewTool(),
    ]
    
    self.tool_registry.register_tools(tools)
```

¡Listo! El agente ahora puede usar tu nueva tool.

## 🔍 Debugging

### Ver qué tools se llaman

Los logs te mostrarán cada vez que el agente usa una tool:

```
INFO:agent:Tool create_mind_task executed successfully
INFO:agent:Mind task created via agent tool: abc123 - 'Meditation'
```

### Probar una tool directamente

```python
from tools.task_tools import CreateMindTaskTool

tool = CreateMindTaskTool()
result = tool.execute(
    user_id="test-123",
    title="Test Task",
    description="Testing...",
    xp_reward=20
)
print(result)
```

## 📝 Estructura de Retorno

Todas las tools deben retornar un dict con:

```python
{
    "success": True,           # ✅ o ❌
    "message": "User message", # Mensaje amigable
    # ... otros datos relevantes
}
```

## 🎨 Plantillas Disponibles

- **`tools/TEMPLATE.py`** - Template completo con comentarios
- **`tools/task_tools.py`** - Ejemplo de tools de creación
- **`tools/query_tools.py`** - Ejemplo de tools de consulta
- **`tools/task_action_tools.py`** - Ejemplo de tools de acción

## 💡 Tips

### Tip 1: Nombres descriptivos
```python
# ❌ Malo
def name(self) -> str:
    return "do_thing"

# ✅ Bueno
def name(self) -> str:
    return "create_user_goal"
```

### Tip 2: Descripciones detalladas
```python
# ❌ Malo
def description(self) -> str:
    return "Creates a goal"

# ✅ Bueno
def description(self) -> str:
    return """Create a long-term goal for the user.
    
Use this when:
- User says "I want to achieve..."
- User asks to set a goal
- User talks about long-term objectives

Example: "I want to lose 10 kg in 3 months"
"""
```

### Tip 3: Validación
```python
def validate_params(self, **kwargs) -> bool:
    user_id = kwargs.get('user_id')
    title = kwargs.get('title')
    
    if not user_id or len(user_id) < 5:
        return False
    
    if not title or len(title) < 3:
        return False
    
    return True
```

## 🐛 Problemas Comunes

### "Tool not found"
- ¿La agregaste a `tools/__init__.py`?
- ¿La registraste en `agent_service.py`?
- ¿Reiniciaste el servidor?

### "Invalid parameters"
- Revisa el schema de `parameters`
- Verifica `validate_params()`
- Chequea los logs del servidor

### "Function call failed"
- Revisa la implementación de `execute()`
- Chequea que los servicios importados existen
- Verifica conexión a base de datos

## 📚 Documentación Completa

- **`README.md`** - Guía completa del sistema
- **`ARCHITECTURE.md`** - Diagramas y arquitectura
- **`EXAMPLES.md`** - Ejemplos de conversaciones
- **`TEMPLATE.py`** - Plantilla con comentarios

## 🎯 Próximos Pasos

1. ✅ Revisar tools existentes en `tools/`
2. ✅ Leer `EXAMPLES.md` para ver casos de uso
3. ✅ Crear tu primera tool usando `TEMPLATE.py`
4. ✅ Probarla con `test_agent_tools.py`
5. ✅ ¡Usarla en producción!

## 🆘 Ayuda

Si tienes problemas:

1. Revisa los logs del servidor
2. Ejecuta `test_agent_tools.py`
3. Lee la documentación en `tools/README.md`
4. Revisa ejemplos en `tools/EXAMPLES.md`
5. Inspecciona una tool similar existente

## 🌟 Ejemplos Rápidos

### Crear tarea de meditación
```python
CreateMindTaskTool().execute(
    user_id="123",
    title="Meditar 10 minutos",
    description="Meditación guiada de respiración",
    xp_reward=20,
    priority="high",
    estimated_duration=10
)
```

### Consultar tareas pendientes
```python
GetUserTasksTool().execute(
    user_id="123",
    task_type="both",
    status="pending"
)
```

### Ver estadísticas
```python
GetUserStatsTool().execute(
    user_id="123"
)
```

---

**¿Listo para crear tu primera tool?** 🚀

Copia `tools/TEMPLATE.py`, modifícalo, y síguelos 3 pasos arriba. ¡Es así de simple!
