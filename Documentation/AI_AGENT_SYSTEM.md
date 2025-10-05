# AI Agent System Documentation

## Overview
Sistema robusto de agentes IA con integración de OpenAI GPT-4 y soporte para Model Context Protocol (MCP). Permite ejecutar acciones complejas mediante lenguaje natural.

## Architecture

### Components

1. **`lib/agent.py`** - Core agent library
   - `AIAgent`: Clase principal del agente con function calling
   - `FunctionRegistry`: Registro de funciones disponibles
   - `AgentConversation`: Gestión de conversaciones y contexto
   - `MultiAgentOrchestrator`: Orquestación de múltiples agentes especializados

2. **`services/agent_service.py`** - Business logic
   - Registro de funciones de base de datos
   - Gestión de contexto de usuario
   - Integración con Supabase

3. **`controllers/agent_controller.py`** - HTTP handlers
   - Endpoints REST para interactuar con agentes
   - Validación de requests

4. **`routes/agent_routes.py`** - URL routing
   - Definición de rutas `/agents/*`

## Features

### ✅ Function Calling
El agente puede ejecutar funciones automáticamente basándose en el contexto:
- Crear, leer, actualizar tareas
- Gestionar objetivos (goals)
- Consultar perfiles y logros
- Estadísticas y analytics

### ✅ Conversational Context
Mantiene contexto de conversación para múltiples usuarios simultáneamente.

### ✅ Multi-Agent Support
Soporte para múltiples agentes especializados con el `MultiAgentOrchestrator`.

### ✅ Robust Error Handling
Manejo completo de errores de API, timeouts, y límites de iteración.

### ✅ Statistics & Monitoring
Métricas de uso, tokens consumidos, y función calls.

## API Endpoints

### 1. Process Agent Request
```http
POST /agents/ask
Content-Type: application/json

{
  "prompt": "Show me all my pending tasks",
  "user_id": 1,
  "conversation_id": "optional_chat_id"
}
```

**Response:**
```json
{
  "success": true,
  "response": "You have 5 pending tasks:\n1. Buy groceries...",
  "function_calls": [
    {
      "function_name": "get_user_tasks",
      "result": {
        "success": true,
        "tasks": [...]
      }
    }
  ],
  "iterations": 2,
  "metadata": {
    "model": "gpt-4-turbo-preview",
    "tokens_used": 350,
    "timestamp": "2025-10-04T10:30:00"
  }
}
```

### 2. Get Agent Statistics
```http
GET /agents/stats
```

**Response:**
```json
{
  "total_requests": 150,
  "successful_requests": 145,
  "failed_requests": 5,
  "total_tokens_used": 50000,
  "total_function_calls": 200,
  "active_conversations": 10,
  "registered_functions": 12
}
```

### 3. List Available Actions
```http
GET /agents/actions
```

**Response:**
```json
{
  "available_functions": [
    "get_user_tasks",
    "create_task",
    "update_task_status",
    "get_user_goals",
    "create_goal",
    "get_user_profile",
    "get_user_achievements",
    "get_task_statistics"
  ],
  "total_functions": 12
}
```

### 4. Clear Conversation
```http
POST /agents/clear
Content-Type: application/json

{
  "user_id": 1,
  "conversation_id": "optional_specific_chat"
}
```

## Usage Examples

### Example 1: Get Tasks
```python
# User says: "Show me my high priority tasks"
# Agent will:
# 1. Call get_user_tasks(user_id=1, status=None)
# 2. Filter by priority="high"
# 3. Return formatted response
```

### Example 2: Create Task
```python
# User says: "Create a task to buy milk tomorrow with high priority"
# Agent will:
# 1. Extract: title="Buy milk", due_date="tomorrow", priority="high"
# 2. Call create_task(user_id=1, title="Buy milk", due_date="2025-10-05", priority="high")
# 3. Confirm creation
```

### Example 3: Complex Query
```python
# User says: "What's my task completion rate this week?"
# Agent will:
# 1. Call get_task_statistics(user_id=1)
# 2. Calculate completion rate
# 3. Return formatted stats
```

## Registering New Functions

Para agregar nuevas funciones al agente:

```python
# En agent_service.py

@self.agent.register_function(
    name="send_notification",
    description="Send a notification to the user",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "integer"},
            "message": {"type": "string"},
            "priority": {"type": "string", "enum": ["low", "medium", "high"]}
        },
        "required": ["user_id", "message"]
    }
)
def send_notification(user_id: int, message: str, priority: str = "medium"):
    # Implementation
    return {"sent": True, "notification_id": 123}
```

## MCP Integration (Future)

El sistema está preparado para integrar Model Context Protocol:

```python
# Future MCP integration example
from lib.agent import AIAgent

agent = AIAgent(name="MCPAgent")

# Register MCP tools
agent.register_mcp_server("database_server", {
    "endpoint": "http://localhost:3000/mcp",
    "tools": ["query_db", "update_db"]
})
```

## Best Practices

### 1. Security
- ✅ Validar `user_id` en cada request
- ✅ Implementar rate limiting
- ✅ No exponer información sensible en prompts

### 2. Performance
- ✅ Usar `conversation_id` para mantener contexto
- ✅ Limpiar conversaciones antiguas periódicamente
- ✅ Monitorear uso de tokens

### 3. Error Handling
- ✅ Siempre devolver `success: false` en errores
- ✅ Incluir mensajes descriptivos
- ✅ Loggear errores para debugging

### 4. Function Design
- ✅ Funciones pequeñas y específicas
- ✅ Descripciones claras para el agente
- ✅ Validación de parámetros

## Environment Variables

```env
OPENAI_API_KEY=sk-proj-...
SUPABASE_URL=https://...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Testing

```bash
# Test agent request
curl -X POST http://localhost:5000/agents/ask \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Show me all my tasks",
    "user_id": 1
  }'

# Test stats
curl http://localhost:5000/agents/stats

# Test available actions
curl http://localhost:5000/agents/actions
```

## Monitoring

Métricas importantes a monitorear:
- Total requests / Tasa de éxito
- Tokens consumidos (costos)
- Tiempo de respuesta promedio
- Function calls más usados
- Conversaciones activas

## Cost Estimation

GPT-4 Turbo Pricing (approximate):
- Input: $0.01 / 1K tokens
- Output: $0.03 / 1K tokens

Average request: ~500 tokens total = $0.015

100 requests/day ≈ $1.50/day ≈ $45/month

## Roadmap

- [ ] Add streaming responses
- [ ] Implement agent memory (long-term)
- [ ] Multi-language support
- [ ] Custom model fine-tuning
- [ ] MCP server integration
- [ ] Agent-to-agent communication
- [ ] Visual task builder
- [ ] Voice input/output

## Support

For issues or questions:
- Check logs: `logger` in each module
- Review function schemas: `GET /agents/actions`
- Test with simple prompts first
