# 🎨 Diagramas Visuales - Sistema de Tools

## 📊 Flujo Completo del Sistema

```
┌──────────────────────────────────────────────────────────────────────┐
│                         FRONTEND / CLIENTE                            │
│                                                                       │
│  Usuario escribe: "Me siento estresado, ¿qué puedo hacer?"          │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ POST /api/chat
                                │ { message, session_id }
                                │ + JWT Token
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                     BACKEND - chat_ia_controller.py                   │
│                                                                       │
│  1. Valida JWT Token                                                 │
│  2. Extrae user_id                                                   │
│  3. Prepara contexto                                                 │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ get_agent_service()
                                │ agent.ask(message, user_context)
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                   AGENT SERVICE - agent_service.py                    │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  AIAgent (lib/agent.py)                                     │    │
│  │  - Mantiene conversación                                    │    │
│  │  - System prompt con instrucciones                          │    │
│  │  - Decide cuándo usar tools                                 │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  ToolRegistry (tools/base_tool.py)                          │    │
│  │  - Gestiona todas las tools registradas                     │    │
│  │  - Conecta tools con el agente                              │    │
│  │  - Proporciona schemas a OpenAI                             │    │
│  └─────────────────────────────────────────────────────────────┘    │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ OpenAI API Call
                                │ + Function schemas
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                          OPENAI GPT-4                                 │
│                                                                       │
│  Analiza el mensaje:                                                 │
│  "Usuario estresado → recomendar meditación → usar create_mind_task" │
│                                                                       │
│  Genera respuesta + function_call:                                   │
│  {                                                                    │
│    "name": "create_mind_task",                                       │
│    "arguments": {                                                    │
│      "user_id": "123",                                               │
│      "title": "Meditación de 10 minutos",                           │
│      "description": "...",                                           │
│      "xp_reward": 20                                                 │
│    }                                                                 │
│  }                                                                   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ Function call result
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                        AGENT - execute_function()                     │
│                                                                       │
│  1. Recibe function_call de OpenAI                                   │
│  2. Busca tool en ToolRegistry                                       │
│  3. Valida parámetros                                                │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    ┌───────────┴──────────┬──────────────────┐
                    ↓                      ↓                  ↓
        ┌───────────────────┐  ┌──────────────────┐  ┌──────────────┐
        │   Task Tools      │  │   Query Tools    │  │ Action Tools │
        │   (task_tools.py) │  │(query_tools.py)  │  │(action_*.py) │
        ├───────────────────┤  ├──────────────────┤  ├──────────────┤
        │CreateMindTaskTool │  │GetUserTasksTool  │  │CompleteTask  │
        │CreateBodyTaskTool │  │GetUserStatsTool  │  │UpdateTask    │
        └─────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘
                  │                     │                    │
                  │ tool.execute()      │                    │
                  └─────────────────────┼────────────────────┘
                                        ↓
┌──────────────────────────────────────────────────────────────────────┐
│                           SERVICES LAYER                              │
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │ mind_task_      │  │ body_task_      │  │ stats_          │    │
│  │ service.py      │  │ service.py      │  │ service.py      │    │
│  │                 │  │                 │  │                 │    │
│  │ create_mind_    │  │ create_body_    │  │ get_user_       │    │
│  │ task()          │  │ task()          │  │ stats()         │    │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘    │
│           │                    │                     │              │
│           └────────────────────┼─────────────────────┘              │
└────────────────────────────────┼──────────────────────────────────────┘
                                 │
                                 │ Supabase Client
                                 │ INSERT/UPDATE/SELECT
                                 ↓
┌──────────────────────────────────────────────────────────────────────┐
│                        SUPABASE DATABASE                              │
│                                                                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ tasks_mind │  │ tasks_body │  │  profiles  │  │   users    │   │
│  ├────────────┤  ├────────────┤  ├────────────┤  ├────────────┤   │
│  │ id         │  │ id         │  │ id         │  │ id         │   │
│  │ user_id    │  │ user_id    │  │ user_id    │  │ email      │   │
│  │ title      │  │ title      │  │ level      │  │ password   │   │
│  │ status     │  │ status     │  │ total_xp   │  │ created_at │   │
│  │ xp_reward  │  │ xp_reward  │  │ streak     │  └────────────┘   │
│  └────────────┘  └────────────┘  └────────────┘                    │
│                                                                       │
│  ✅ INSERT INTO tasks_mind VALUES (...)                              │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ Success response
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                        TOOL - Response                                │
│                                                                       │
│  {                                                                    │
│    "success": true,                                                  │
│    "task_id": "abc-123",                                             │
│    "message": "✅ Tarea 'Meditación' creada!"                        │
│  }                                                                   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ Tool result
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                     AGENT - Generate Final Response                   │
│                                                                       │
│  1. Recibe resultado de la tool                                      │
│  2. Envía de vuelta a OpenAI con el resultado                        │
│  3. OpenAI genera respuesta final natural                            │
│                                                                       │
│  Respuesta: "He agregado 'Meditación de 10 minutos' a tus tareas    │
│             mentales. Ganarás 20 XP al completarla. ¿Cómo te         │
│             gustaría que te ayude a prepararte para meditar?"        │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ JSON Response
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                         CONTROLLER - Response                         │
│                                                                       │
│  {                                                                    │
│    "content": "He agregado 'Meditación de 10 minutos'...",          │
│    "session_id": "session-123",                                      │
│    "function_calls_made": 1,                                         │
│    "function_results": [...]                                         │
│  }                                                                   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ HTTP 200 OK
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│                         FRONTEND - Display                            │
│                                                                       │
│  Usuario ve:                                                         │
│  "He agregado 'Meditación de 10 minutos' a tus tareas mentales.     │
│   Ganarás 20 XP al completarla..."                                  │
│                                                                       │
│  ✅ La tarea aparece automáticamente en su lista                     │
└──────────────────────────────────────────────────────────────────────┘
```

## 🔄 Ciclo de Vida de una Tool

```
REGISTRO (Inicio del servidor)
══════════════════════════════

   ┌─────────────────┐
   │  app.py start   │
   └────────┬────────┘
            │
            ↓
   ┌─────────────────────┐
   │ Import routes       │
   │ Import controllers  │
   │ Import services     │
   └────────┬────────────┘
            │
            ↓
   ┌──────────────────────────┐
   │ agent_service.__init__() │
   └────────┬─────────────────┘
            │
            ↓
   ┌──────────────────────────┐
   │ AIAgent()                │
   │ - system_prompt          │
   │ - model: gpt-4-turbo     │
   └────────┬─────────────────┘
            │
            ↓
   ┌──────────────────────────┐
   │ ToolRegistry(agent)      │
   └────────┬─────────────────┘
            │
            ↓
   ┌──────────────────────────┐
   │ _register_tools()        │
   └────────┬─────────────────┘
            │
            ├──→ CreateMindTaskTool()
            ├──→ CreateBodyTaskTool()
            ├──→ GetUserTasksTool()
            └──→ GetUserStatsTool()
            │
            ↓
   ┌──────────────────────────┐
   │ tool_registry.           │
   │ register_tools()         │
   └────────┬─────────────────┘
            │
            ↓
   ┌──────────────────────────┐
   │ For each tool:           │
   │ - Get schema             │
   │ - Create wrapper         │
   │ - Register with agent    │
   └────────┬─────────────────┘
            │
            ↓
   ┌──────────────────────────┐
   │ ✅ Server ready          │
   │ Tools: [4]               │
   │ Agent: Active            │
   └──────────────────────────┘


EJECUCIÓN (Durante conversación)
═══════════════════════════════

   ┌──────────────────────┐
   │ User sends message   │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ agent.ask()          │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ OpenAI analyzes      │
   │ Decides: use tool    │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ Returns function_call│
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ agent.execute_       │
   │ function()           │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ tool_registry.       │
   │ get_function()       │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ tool.validate_       │
   │ params()             │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ tool.execute()       │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ Service layer        │
   │ (DB operations)      │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ Return result        │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ Send to OpenAI       │
   │ with result          │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ OpenAI generates     │
   │ final response       │
   └──────────┬───────────┘
              │
              ↓
   ┌──────────────────────┐
   │ ✅ User gets answer  │
   └──────────────────────┘
```

## 🏗️ Arquitectura de Clases

```
                    ┌─────────────────┐
                    │   BaseTool      │
                    │   (Abstract)    │
                    ├─────────────────┤
                    │ + name          │
                    │ + description   │
                    │ + parameters    │
                    │ + execute()     │
                    │ + validate()    │
                    │ + on_error()    │
                    └────────┬────────┘
                             │
                             │ inherits
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ↓                  ↓                  ↓
┌──────────────────┐ ┌──────────────┐ ┌──────────────┐
│CreateMindTaskTool│ │GetUserTasks  │ │CompleteTask  │
├──────────────────┤ │Tool          │ │Tool          │
│+ name            │ ├──────────────┤ ├──────────────┤
│+ description     │ │+ name        │ │+ name        │
│+ parameters      │ │+ description │ │+ description │
│+ execute()       │ │+ parameters  │ │+ parameters  │
│                  │ │+ execute()   │ │+ execute()   │
└──────────────────┘ └──────────────┘ └──────────────┘


     ┌────────────────────────────────┐
     │      ToolRegistry              │
     ├────────────────────────────────┤
     │ - agent: AIAgent               │
     │ - tools: Dict[str, BaseTool]   │
     ├────────────────────────────────┤
     │ + register_tool(tool)          │
     │ + register_tools(tools)        │
     │ + get_tool(name)               │
     │ + list_tools()                 │
     │ + get_tool_info()              │
     └────────────┬───────────────────┘
                  │
                  │ manages
                  ↓
          ┌───────────────┐
          │   AIAgent     │
          ├───────────────┤
          │ + ask()       │
          │ + execute_    │
          │   function()  │
          └───────────────┘
```

## 📦 Dependencias del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND APP                            │
│                    (React/Vue/etc)                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/REST
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                         │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌───────────────┐        │
│  │ Routes     │→ │Controllers │→ │ Services      │        │
│  └────────────┘  └────────────┘  └───────┬───────┘        │
│                                            │                 │
│  ┌──────────────────────────────────────┐ │                │
│  │         Agent Service                 │←┘                │
│  │  ┌────────────────────────────────┐  │                  │
│  │  │        AIAgent                 │  │                  │
│  │  │  ┌──────────────────────────┐  │  │                  │
│  │  │  │    ToolRegistry          │  │  │                  │
│  │  │  │  ┌────────────────────┐  │  │  │                  │
│  │  │  │  │  Tools Collection  │  │  │  │                  │
│  │  │  │  └────────────────────┘  │  │  │                  │
│  │  │  └──────────────────────────┘  │  │                  │
│  │  └────────────────────────────────┘  │                  │
│  └──────────────────┬────────────────────┘                  │
└─────────────────────┼───────────────────────────────────────┘
                      │
          ┌───────────┼──────────────┐
          │           │              │
          ↓           ↓              ↓
    ┌──────────┐ ┌─────────┐ ┌──────────────┐
    │ OpenAI   │ │Supabase │ │Python Stdlib │
    │ API      │ │Database │ │   + Libs     │
    └──────────┘ └─────────┘ └──────────────┘
    
    Dependencies:
    - openai
    - supabase-py
    - python-dotenv
    - flask
    - pyjwt
    - bcrypt
```

## 🔀 Flujo de Decisión del Agente

```
        Mensaje del Usuario
                │
                ↓
        ┌───────────────┐
        │ Analizar con  │
        │   OpenAI      │
        └───────┬───────┘
                │
                ↓
        ¿Necesita acción?
                │
        ┌───────┴───────┐
        │               │
       SI              NO
        │               │
        ↓               ↓
  ┌──────────┐   ┌──────────┐
  │ Function │   │ Respuesta│
  │   Call   │   │  Directa │
  └────┬─────┘   └────┬─────┘
       │              │
       ↓              │
  ¿Qué tool?         │
       │              │
  ┌────┼─────┐        │
  │    │     │        │
  ↓    ↓     ↓        │
 Mind Body Query     │
 Task Task  Info     │
  │    │     │        │
  └────┴─────┴────────┘
          │
          ↓
    Ejecutar Tool
          │
          ↓
   ¿Éxito?
          │
    ┌─────┴─────┐
   SI          NO
    │           │
    ↓           ↓
 Confirmar   Reportar
  Acción      Error
    │           │
    └─────┬─────┘
          │
          ↓
    Respuesta al
       Usuario
```

---

**Estos diagramas te ayudarán a entender visualmente cómo funciona el sistema.** 📊✨
