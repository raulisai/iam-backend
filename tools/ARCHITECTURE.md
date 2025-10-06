# Arquitectura del Sistema de Tools del Agente IA

## Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────┐
│                         USUARIO                              │
│                 (Envía mensaje al chat)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  chat_ia_controller.py                       │
│              (Recibe mensaje y contexto)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  services/agent_service.py                   │
│  ┌────────────────────────────────────────────────────┐     │
│  │  AIAgent (lib/agent.py)                            │     │
│  │  - Recibe prompt y contexto                        │     │
│  │  - Decide si usar tools                            │     │
│  │  - Llama a OpenAI con function calling             │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  ToolRegistry (tools/base_tool.py)                 │     │
│  │  - Gestiona todas las tools registradas            │     │
│  │  - Conecta tools con el agente                     │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        │            │            │              │
        ▼            ▼            ▼              ▼
┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐
│ Task Tools  │ │ Query   │ │ Action   │ │  Future     │
│             │ │ Tools   │ │ Tools    │ │  Tools      │
├─────────────┤ ├─────────┤ ├──────────┤ ├──────────────┤
│• Create     │ │• Get    │ │• Complete│ │• Goals      │
│  Mind Task  │ │  Tasks  │ │  Task    │ │• Reminders  │
│             │ │         │ │          │ │• Reports    │
│• Create     │ │• Get    │ │• Update  │ │• Analytics  │
│  Body Task  │ │  Stats  │ │  Task    │ │• Etc...     │
└──────┬──────┘ └────┬────┘ └─────┬────┘ └──────────────┘
       │             │            │
       └─────────────┼────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVICIOS                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │ mind_task_   │ │ body_task_   │ │ stats_service    │    │
│  │ service      │ │ service      │ │                  │    │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘    │
└─────────┼────────────────┼──────────────────┼──────────────┘
          │                │                  │
          └────────────────┼──────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPABASE DATABASE                         │
│  - tasks_mind                                                │
│  - tasks_body                                                │
│  - profiles                                                  │
│  - etc...                                                    │
└─────────────────────────────────────────────────────────────┘
```

## Flujo de Ejecución de una Tool

```
1. Usuario: "Me siento estresado"
         ↓
2. Controller recibe mensaje + user_id
         ↓
3. AgentService.agent.ask()
         ↓
4. OpenAI analiza el mensaje y el contexto
         ↓
5. OpenAI decide: "Debería recomendar meditación y crearla"
         ↓
6. OpenAI genera function_call:
   {
     "name": "create_mind_task",
     "arguments": {
       "user_id": "123",
       "title": "Meditación de 10 minutos",
       "description": "...",
       "xp_reward": 20
     }
   }
         ↓
7. Agent ejecuta: tool_registry → CreateMindTaskTool.execute()
         ↓
8. Tool llama: mind_task_service.create_mind_task()
         ↓
9. Service guarda en Supabase
         ↓
10. Tool retorna: {"success": true, "message": "✅ Task created!"}
         ↓
11. Agent recibe resultado y genera respuesta final
         ↓
12. Usuario recibe: "He agregado 'Meditación de 10 minutos' a tus tareas!"
```

## Estructura de Clases

```python
BaseTool (ABC)
├── @property name: str
├── @property description: str
├── @property parameters: Dict
├── validate_params(**kwargs) -> bool
├── execute(**kwargs) -> Dict
└── on_error(error) -> Dict

ToolRegistry
├── __init__(agent: AIAgent)
├── register_tool(tool: BaseTool)
├── register_tools(tools: List[BaseTool])
├── get_tool(name: str) -> BaseTool
├── list_tools() -> List[str]
└── get_tool_info() -> List[Dict]

CreateMindTaskTool(BaseTool)
├── name = "create_mind_task"
├── description = "Create mental tasks..."
├── parameters = {...}
└── execute(**kwargs) -> Dict

CreateBodyTaskTool(BaseTool)
├── name = "create_body_task"
├── description = "Create physical tasks..."
├── parameters = {...}
└── execute(**kwargs) -> Dict

GetUserTasksTool(BaseTool)
├── name = "get_user_tasks"
├── description = "Retrieve user tasks..."
├── parameters = {...}
└── execute(**kwargs) -> Dict

# ... más tools
```

## Ciclo de Vida de una Tool

```
REGISTRO (Al iniciar el servidor)
─────────────────────────────────
1. AgentService.__init__()
2. agent = AIAgent(...)
3. tool_registry = ToolRegistry(agent)
4. _register_tools()
5. tools = [CreateMindTaskTool(), ...]
6. tool_registry.register_tools(tools)
7. Cada tool → agent.register_function()

EJECUCIÓN (Durante una conversación)
────────────────────────────────────
1. Usuario envía mensaje
2. Agent.ask(prompt, user_context)
3. OpenAI analiza y decide usar tool
4. Agent.execute_function(name, args)
5. tool_registry → Tool.execute()
6. Tool → Service → Database
7. Tool retorna resultado
8. Agent genera respuesta con resultado
9. Usuario recibe respuesta
```

## Ventajas de esta Arquitectura

### ✅ Modular y Escalable
- Cada tool es independiente
- Fácil agregar nuevas tools sin modificar existentes
- Separación clara de responsabilidades

### ✅ Reutilizable
- BaseTool proporciona estructura común
- ToolRegistry gestiona automáticamente el registro
- Template facilita creación de nuevas tools

### ✅ Mantenible
- Código organizado por funcionalidad
- Validación y error handling consistentes
- Logging en todos los niveles

### ✅ Testeable
- Cada tool se puede probar independientemente
- Mock services para testing unitario
- Script de prueba incluido

### ✅ Extensible
- Simple agregar nuevos tipos de tools
- Fácil modificar comportamiento con herencia
- Hooks para validación y error handling

## Ejemplo de Extensión

### Agregar una nueva categoría de tools:

```python
# 1. Crear tools/notification_tools.py
class SendNotificationTool(BaseTool):
    @property
    def name(self) -> str:
        return "send_notification"
    
    # ... implementación

# 2. Actualizar tools/__init__.py
from .notification_tools import SendNotificationTool
__all__ = [..., 'SendNotificationTool']

# 3. Registrar en agent_service.py
def _register_tools(self):
    tools = [
        # ... existing tools
        SendNotificationTool(),
    ]
```

## Mejores Prácticas

1. **Una Tool, Una Responsabilidad**
   - Cada tool hace una cosa específica
   - No mezclar funcionalidades diferentes

2. **Descripciones Detalladas**
   - El agente usa la descripción para decidir
   - Incluir casos de uso y ejemplos

3. **Validación Robusta**
   - Validar parámetros antes de ejecutar
   - Retornar errores claros

4. **Error Handling**
   - Try/catch en execute()
   - Logging de errores
   - Mensajes amigables al usuario

5. **Testing**
   - Probar cada tool individualmente
   - Probar integración con el agente
   - Probar casos edge

6. **Documentación**
   - Comentarios en el código
   - Ejemplos de uso
   - Actualizar README cuando agregues tools

## Métricas y Monitoreo

Puedes agregar métricas para monitorear el uso de tools:

```python
# En BaseTool
import time

def execute(self, **kwargs):
    start_time = time.time()
    try:
        result = self._execute_impl(**kwargs)
        duration = time.time() - start_time
        logger.info(f"Tool {self.name} executed in {duration:.2f}s")
        return result
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Tool {self.name} failed after {duration:.2f}s")
        raise
```

## Seguridad

Consideraciones de seguridad:

1. **Validación de user_id**: Siempre verificar que el user_id en los parámetros coincida con el user_context
2. **Permisos**: Verificar permisos antes de ejecutar acciones
3. **Rate Limiting**: Limitar número de tool calls por usuario
4. **Sanitización**: Validar y sanitizar inputs del usuario
5. **Auditoría**: Loggear todas las acciones importantes

```python
def execute(self, **kwargs):
    # Verificar user_id
    user_id = kwargs.get('user_id')
    context_user_id = get_context_user_id()  # From middleware
    
    if user_id != context_user_id:
        raise SecurityError("User ID mismatch")
    
    # Continuar con ejecución...
```
