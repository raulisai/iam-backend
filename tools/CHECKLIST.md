# ✅ Checklist de Instalación - Sistema de Tools

## Verificación de Archivos

### Carpeta `tools/`
- [ ] `__init__.py` - Exports de todas las tools
- [ ] `base_tool.py` - Clase base BaseTool y ToolRegistry
- [ ] `task_tools.py` - CreateMindTaskTool y CreateBodyTaskTool
- [ ] `query_tools.py` - GetUserTasksTool y GetUserStatsTool
- [ ] `task_action_tools.py` - CompleteTaskTool y UpdateTaskTool
- [ ] `TEMPLATE.py` - Plantilla para nuevas tools
- [ ] `README.md` - Documentación completa
- [ ] `QUICKSTART.md` - Guía de inicio rápido
- [ ] `EXAMPLES.md` - Ejemplos de uso
- [ ] `ARCHITECTURE.md` - Diagramas de arquitectura
- [ ] `CHECKLIST.md` - Este archivo

### Archivos Modificados
- [ ] `services/agent_service.py` - Actualizado con ToolRegistry

### Archivos de Test
- [ ] `test/test_agent_tools.py` - Script de prueba del sistema

## Verificación de Funcionalidad

### 1. Imports
```bash
python -c "from tools import BaseTool, ToolRegistry; print('✅ Imports OK')"
```
Debería imprimir: ✅ Imports OK

### 2. Tool Creation
```bash
python -c "from tools import CreateMindTaskTool; tool = CreateMindTaskTool(); print(f'✅ Tool name: {tool.name}')"
```
Debería imprimir: ✅ Tool name: create_mind_task

### 3. Agent Service
```bash
python -c "from services.agent_service import get_agent_service; service = get_agent_service(); print(f'✅ Tools registered: {len(service.tool_registry.list_tools())}')"
```
Debería imprimir: ✅ Tools registered: 4 (o más)

### 4. Full Test
```bash
python test/test_agent_tools.py
```
Debería mostrar: ✅ All tests passed!

## Verificación de Dependencias

### Python Packages
- [ ] `openai` - Para el agente de IA
- [ ] `python-dotenv` - Para variables de entorno
- [ ] `supabase` - Para base de datos

Verificar:
```bash
pip list | grep -E "(openai|python-dotenv|supabase)"
```

### Variables de Entorno
- [ ] `OPENAI_API_KEY` - Clave de OpenAI
- [ ] `SUPABASE_URL` - URL de Supabase
- [ ] `SUPABASE_KEY` - Clave de Supabase

Verificar:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING')"
```

## Verificación de Servicios

### Services Directory
- [ ] `services/mind_task_service.py` - Existe y tiene create_mind_task()
- [ ] `services/body_task_service.py` - Existe y tiene create_body_task()
- [ ] `services/stats_service.py` - Existe y tiene get_user_stats()

Verificar:
```bash
python -c "from services.mind_task_service import create_mind_task; print('✅ mind_task_service OK')"
```

## Verificación de Integración

### 1. Controller Integration
Verificar que el controller usa el agent service:

```python
# En controllers/chat_ia_controller.py
from services.agent_service import get_agent_service

agent_service = get_agent_service()
```

### 2. User Context
Verificar que se pasa el user_id en el contexto:

```python
response = await agent_service.agent.ask(
    message,
    conversation_id=session_id,
    user_context={"user_id": user_id}
)
```

## Tests Manuales

### Test 1: Crear Tarea Mental
```bash
# Iniciar servidor
python app.py

# En otra terminal, hacer request al chat
curl -X POST http://localhost:5000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Me siento estresado, ¿qué puedo hacer?",
    "session_id": "test-session"
  }'
```

Respuesta esperada:
- El agente recomienda meditación
- Pregunta si quiere agregarla
- Usuario confirma
- Agente crea la tarea

### Test 2: Consultar Tareas
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué tareas tengo pendientes?",
    "session_id": "test-session"
  }'
```

Respuesta esperada:
- El agente lista las tareas pendientes

### Test 3: Ver Estadísticas
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cómo voy en mi progreso?",
    "session_id": "test-session"
  }'
```

Respuesta esperada:
- El agente muestra las estadísticas

## Problemas Comunes

### ❌ "Unable to import 'tools.base_tool'"
**Solución**: Asegúrate de que existe `tools/__init__.py` y que no hay errores de sintaxis

### ❌ "Tool not found"
**Solución**: 
1. Verifica que la tool está en `tools/__init__.py`
2. Verifica que está registrada en `agent_service.py`
3. Reinicia el servidor

### ❌ "Invalid parameters"
**Solución**: 
1. Revisa el schema de parameters en la tool
2. Verifica que user_id se pasa en user_context
3. Chequea los logs para ver qué parámetros se enviaron

### ❌ "OpenAI API error"
**Solución**: 
1. Verifica que OPENAI_API_KEY está configurada
2. Verifica que tienes créditos en OpenAI
3. Chequea que el modelo existe (gpt-4-turbo-preview)

### ❌ "Database connection error"
**Solución**: 
1. Verifica SUPABASE_URL y SUPABASE_KEY
2. Verifica que las tablas existen en Supabase
3. Chequea permisos de las tablas

## Logs de Verificación

Cuando el servidor inicia, deberías ver:

```
INFO:agent_service:Agent service initialized with 4 tools
INFO:agent_service:Registered tools: create_mind_task, create_body_task, get_user_tasks, get_user_stats
INFO:agent:Agent initialized: WellnessProductivityAssistant
```

Cuando se usa una tool:

```
INFO:agent:Tool create_mind_task called with parameters: {...}
INFO:mind_task_service:Mind task created via agent tool: abc123 - 'Meditation'
INFO:agent:Tool create_mind_task executed successfully
```

## Métricas de Éxito

### Nivel 1: Básico ✅
- [ ] Imports funcionan
- [ ] Tools se crean sin errores
- [ ] Agent service se inicializa
- [ ] Tools se registran

### Nivel 2: Funcional ✅✅
- [ ] Test script pasa completamente
- [ ] Tools se pueden ejecutar manualmente
- [ ] Servicios responden correctamente
- [ ] Base de datos conecta

### Nivel 3: Integración ✅✅✅
- [ ] Chat endpoint funciona
- [ ] Agente recibe mensajes
- [ ] Agente llama tools automáticamente
- [ ] Tasks se crean en la BD

### Nivel 4: Producción ✅✅✅✅
- [ ] Conversaciones naturales funcionan
- [ ] Agente responde en el idioma correcto
- [ ] Tools se usan apropiadamente
- [ ] Usuarios satisfechos

## Próximos Pasos

Una vez que todo esté ✅:

1. 📝 Leer `QUICKSTART.md` para empezar a usar el sistema
2. 🎨 Revisar `EXAMPLES.md` para ver casos de uso
3. 🔧 Crear tu primera tool con `TEMPLATE.py`
4. 🚀 ¡Deploy a producción!

---

**Fecha de verificación**: _____________

**Verificado por**: _____________

**Notas adicionales**:
```
_____________________________________________
_____________________________________________
_____________________________________________
```
