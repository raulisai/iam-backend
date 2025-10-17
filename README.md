# IAM Backend - Sistema de Gestión de Tareas y Bienestar

Backend completo desarrollado en Flask con autenticación JWT, gestión de tareas (mente y cuerpo), perfiles de usuario, logros, metas, chat IA y sistema de bot automatizado.

## 🚀 Características Principales

- ✅ **Autenticación JWT** - Sistema seguro de autenticación con tokens
- ✅ **Gestión de Perfiles** - Perfiles personalizados de usuario
- ✅ **Sistema de Tareas** - Tareas de mente y cuerpo con plantillas reutilizables
- ✅ **Logros y Metas** - Sistema de gamificación y objetivos
- ✅ **Chat IA Inteligente** - Agente de IA con capacidades de acción (OpenAI)
- ✅ **Sistema de Tools Extensible** - El agente puede crear tareas, consultar info y más
- ✅ **Bot Rules** - Sistema de reglas automáticas configurable
- ✅ **Registro de Actividades** - Logs y tracking de fallos
- ✅ **Time Optimizer** - Sistema inteligente de optimización de horarios y tareas
- ✅ **Sistema de Automatización** - Tareas programadas con GitHub Actions (scores, notificaciones, métricas)
- ✅ **Swagger UI** - Documentación interactiva de API

## 📋 Requisitos

- Python 3.8+
- Flask
- Supabase (PostgreSQL)
- PyJWT
- Bcrypt
- Flasgger (Swagger)

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd iam-backend
```

### 2. Crear y activar entorno virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install flask flask-cors flasgger supabase pyjwt bcrypt openai python-dotenv
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz:
```env
JWT_SECRET_KEY=tu-secret-key-super-segura-aqui
SUPABASE_URL=tu-supabase-project-url
SUPABASE_KEY=tu-supabase-anon-key
OPENAI_API_KEY=tu-openai-api-key-aqui
```

### 5. Crear las tablas en Supabase
Ejecutar los scripts SQL proporcionados en tu base de datos Supabase para crear todas las tablas necesarias.

## 🎯 Uso

### Ejecutar el servidor
```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

### Acceder a Swagger UI
Abrir en el navegador: `http://localhost:5000/apidocs/`

## 📚 Documentación

### API y Autenticación
- **[API_DOCUMENTATION.md](Documentation/API_DOCUMENTATION.md)** - Documentación completa de endpoints
- **[JWT_AUTHENTICATION.md](Documentation/JWT_AUTHENTICATION.md)** - Guía de autenticación JWT
- **[IMPLEMENTATION_SUMMARY.md](Documentation/IMPLEMENTATION_SUMMARY.md)** - Resumen técnico de implementación

### Sistema de Agente IA
- **[AGENT_TOOLS_SUMMARY.md](AGENT_TOOLS_SUMMARY.md)** - 🤖 Resumen del sistema de tools
- **[tools/QUICKSTART.md](tools/QUICKSTART.md)** - 🚀 Inicio rápido con tools
- **[tools/README.md](tools/README.md)** - 📚 Guía completa del sistema de tools
- **[tools/ARCHITECTURE.md](tools/ARCHITECTURE.md)** - 🏗️ Arquitectura del sistema
- **[tools/EXAMPLES.md](tools/EXAMPLES.md)** - 💬 Ejemplos de conversaciones

### Sistema de Optimización de Tiempo ⚡ NUEVO
- **[TIME_OPTIMIZER_QUICKSTART.md](Documentation/TIME_OPTIMIZER_QUICKSTART.md)** - ⚡ Guía rápida de uso
- **[TIME_OPTIMIZER_SYSTEM.md](Documentation/TIME_OPTIMIZER_SYSTEM.md)** - 📖 Documentación técnica completa
- **[TIME_OPTIMIZER_DIAGRAMS.md](Documentation/TIME_OPTIMIZER_DIAGRAMS.md)** - 📊 Diagramas y visualizaciones
- **[TIME_OPTIMIZER_CURL_EXAMPLES.md](Documentation/TIME_OPTIMIZER_CURL_EXAMPLES.md)** - 🧪 Ejemplos cURL

### Sistema de Automatización 🤖 NUEVO
- **[AUTOMATION_SUMMARY.md](AUTOMATION_SUMMARY.md)** - 📋 Resumen ejecutivo del sistema
- **[AUTOMATION_SETUP.md](AUTOMATION_SETUP.md)** - 🔧 Guía de configuración paso a paso
- **[automation/README.md](automation/README.md)** - 📚 Documentación técnica completa
- **[automation/ARCHITECTURE.md](automation/ARCHITECTURE.md)** - 🏗️ Arquitectura del sistema
- **[automation/EXAMPLES.md](automation/EXAMPLES.md)** - 💡 Ejemplos de uso y casos comunes

## 🏗️ Estructura del Proyecto

```
iam-backend/
├── app.py                    # Aplicación principal
├── middleware/               # Middleware de autenticación
├── services/                 # Lógica de negocio
│   └── agent_service.py      # Servicio del agente IA
├── controllers/              # Controladores HTTP
├── routes/                   # Definición de rutas
├── lib/                      # Utilidades (DB, agente IA)
│   ├── agent.py              # Motor del agente IA
│   └── db.py                 # Conexión a base de datos
├── tools/                    # Sistema de Tools del Agente
│   ├── base_tool.py          # Clase base y registro
│   ├── task_tools.py         # Tools de creación de tareas
│   ├── query_tools.py        # Tools de consulta
│   ├── task_action_tools.py  # Tools de acciones
│   ├── TEMPLATE.py           # Plantilla para nuevas tools
│   └── *.md                  # Documentación completa
├── automation/               # 🆕 Sistema de Automatización
│   ├── scheduler.py          # Orquestador principal
│   ├── score_calculator.py   # Cálculo de scores
│   ├── notification_sender.py# Envío de notificaciones
│   ├── metrics_updater.py    # Actualización de métricas
│   └── *.md                  # Documentación completa
├── scripts/                  # Scripts ejecutables
│   ├── run_automation.py     # Script para GitHub Actions
│   └── manage_automation.py  # Utilidades de gestión
├── .github/workflows/        # GitHub Actions
│   └── hourly_automation.yml # Workflow horario
└── Documentation/            # Documentación del proyecto
```

## 🔐 Autenticación

### Obtener Token JWT
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Usar Token en Requests
```bash
curl -X GET http://localhost:5000/api/profile \
  -H "Authorization: Bearer <your-jwt-token>"
```

## 📡 Endpoints Principales

### Autenticación
- `POST /login` - Iniciar sesión

### Perfiles
- `GET /api/profile` - Obtener perfil
- `POST /api/profile` - Crear perfil
- `PUT /api/profile` - Actualizar perfil

### Tareas
- `GET /api/tasks/mind` - Obtener tareas de mente
- `GET /api/tasks/body` - Obtener tareas de cuerpo
- `POST /api/tasks/mind` - Crear tarea de mente
- `POST /api/tasks/body` - Crear tarea de cuerpo

### Plantillas
- `GET /api/task-templates` - Obtener plantillas
- `GET /api/task-templates/category/mind` - Plantillas de mente
- `GET /api/task-templates/category/body` - Plantillas de cuerpo

### Logros y Metas
- `GET /api/achievements` - Obtener logros
- `GET /api/goals` - Obtener metas

### Chat IA con Agente Inteligente
- `POST /api/chat` - Enviar mensaje al agente IA
- `GET /api/chat/sessions` - Obtener sesiones de chat
- `POST /api/chat/sessions` - Crear sesión
- `GET /api/chat/sessions/<id>/messages` - Obtener mensajes

### Time Optimizer ⚡ NUEVO
- `GET /api/time-optimizer/available-time` - Calcular tiempo disponible
- `GET /api/time-optimizer/optimize-day` - Generar horario optimizado del día
- `GET /api/time-optimizer/tasks-now` - Obtener tareas recomendadas para AHORA
- `GET /api/time-optimizer/remaining-day` - Ver qué falta del día

#### 🤖 Capacidades del Agente IA

El agente puede realizar acciones automáticamente:
- ✅ Crear tareas de mente y cuerpo cuando las recomienda
- ✅ Consultar tareas pendientes del usuario
- ✅ Obtener estadísticas y progreso
- ✅ Completar y actualizar tareas
- ✅ Responder en el idioma del usuario (español/inglés)

Ver [AGENT_TOOLS_SUMMARY.md](AGENT_TOOLS_SUMMARY.md) para más información.

### ⚡ Time Optimizer - Optimización Inteligente de Horarios

El sistema de optimización de tiempo es un **algoritmo sofisticado** que maximiza tu productividad calculando el tiempo real disponible y distribuyendo tareas de forma óptima.

#### 🎯 ¿Qué hace?

1. **Calcula tu tiempo disponible real**
   - Resta horas fijas: trabajo (8h), sueño (8h), cuidado personal (2h)
   - Identifica slots productivos: mañana (6am-9am) y tarde (5pm-10pm)
   
2. **Prioriza tareas inteligentemente**
   - **Goals con deadline cercano** → Máxima prioridad
   - **Goals regulares** → Alta prioridad
   - **Mind/Body tasks** → Media prioridad
   
3. **Distribuye tareas óptimamente**
   - Tareas de concentración (goals/mind) → Mañana
   - Tareas físicas (body) → Tarde
   - Respeta límite semanal de horas de estudio

#### 🚀 Casos de Uso

```python
# 1. Planificar el día (por la mañana)
GET /api/time-optimizer/optimize-day
# → Lista completa de tareas con horarios específicos

# 2. "¿Qué hago ahora?" (cualquier momento)
GET /api/time-optimizer/tasks-now
# → Top 3-5 tareas recomendadas para ESTE momento

# 3. "¿Qué me falta?" (revisar progreso)
GET /api/time-optimizer/remaining-day
# → Tareas pendientes y si puedes completar todo hoy
```

#### 📊 Ejemplo Real

**Input**: Usuario con 5 tareas pendientes
- 🎯 Proyecto ML (90min) - vence mañana
- 🎯 Revisar código (45min) - vence en 2 días
- 🎯 Estudiar capítulo 3 (60min)
- 🧘 Meditación (30min)
- 💪 Gym (60min)

**Output del Algoritmo**:
```
MAÑANA (6:00-9:00):
  06:00-07:30 | Proyecto ML (URGENTE - vence mañana)

TARDE (17:00-22:00):
  17:00-17:45 | Revisar código
  18:00-19:00 | Estudiar capítulo 3
  19:15-19:45 | Meditación
  20:00-21:00 | Gym

Scores:
  ✓ Efficiency: 67.9% (tiempo bien utilizado)
  ✓ Balance: 95.0% (excelente distribución)
  ✓ Productivity: 76.4% (buena productividad)
```

#### 🔥 Características Clave

- ✅ **Considera deadlines**: Tareas urgentes van primero automáticamente
- ✅ **Optimiza por hora del día**: Tasks mentales por la mañana, físicas por la tarde
- ✅ **Respeta límites**: No excede tus horas semanales disponibles
- ✅ **Incluye buffers**: 15 minutos entre tareas para descansar
- ✅ **Scoring inteligente**: Combina tipo de tarea, urgencia y duración

#### 📚 Documentación Completa

Ver [TIME_OPTIMIZER_QUICKSTART.md](Documentation/TIME_OPTIMIZER_QUICKSTART.md) para empezar.

Ver documentación completa en [API_DOCUMENTATION.md](Documentation/API_DOCUMENTATION.md)

### 🤖 Sistema de Automatización - Tareas Programadas con GitHub Actions

El sistema de automatización ejecuta tareas programadas cada hora mediante GitHub Actions para mantener el sistema funcionando de forma autónoma.

#### 🎯 ¿Qué hace?

**Cada Hora (0 * * * *):**
- ✅ Envía notificaciones programadas (alarmas y recordatorios de rutina)
- ✅ Actualiza métricas de rendimiento de usuarios
- ✅ Rastrea tasas de completación de tareas

**Al Final del Día (23:00):**
- ✅ Calcula scores diarios (Body y Mind)
- ✅ Aplica penalizaciones por tareas incompletas
- ✅ Envía resúmenes diarios a usuarios

**Semanalmente (Domingo 00:00):**
- ✅ Limpia snapshots antiguos (>90 días)
- ✅ Genera reportes semanales de rendimiento

#### 📊 Sistema de Scores

**Penalizaciones Automáticas:**
```
Tarea Body incompleta:    -5 puntos
Tarea Mind incompleta:    -5 puntos
Alarma de rutina perdida: -3 puntos
Score mínimo:              0 puntos
```

**Ejemplo:**
```
Usuario con 2 tareas Body pendientes y 1 Mind pendiente:
- Penalty Body: 2 × 5 = -10 puntos
- Penalty Mind: 1 × 5 = -5 puntos
- Total: -15 puntos

Score inicial: Body=100, Mind=100
Score final:   Body=90,  Mind=95
```

#### 🔔 Notificaciones Inteligentes

**Alarmas de Rutina:**
- Horario específico (ej: 7:00 AM)
- Días de la semana configurables
- Notificaciones push via Firebase FCM

**Recordatorios Distribuidos:**
- Múltiples veces al día (ej: 8 veces)
- Distribuidos en ventana de tiempo (ej: 8 AM - 10 PM)
- Intervalo automático calculado

#### 🚀 Configuración Rápida

1. **Configurar Secrets en GitHub:**
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `FIREBASE_SERVICE_ACCOUNT`
   - `JWT_SECRET_KEY`

2. **Push al repositorio:**
   ```bash
   git push origin main
   ```

3. **El workflow se ejecuta automáticamente cada hora**

#### 📈 Métricas Rastreadas

```json
{
  "completed_body_tasks": 5,
  "completed_mind_tasks": 3,
  "body_completion_rate": 71.43,
  "mind_completion_rate": 75.0,
  "score_body": 90,
  "score_mind": 95,
  "active_alarms": 4,
  "active_reminders": 6
}
```

#### 🛠️ Comandos Útiles

```bash
# Ejecutar localmente
python scripts/run_automation.py

# Ejecutar tarea específica
python scripts/run_automation.py notifications
python scripts/run_automation.py metrics
python scripts/run_automation.py scores

# Ver snapshots recientes
python scripts/manage_automation.py snapshots

# Ver rutinas activas
python scripts/manage_automation.py routines
```

#### 📚 Documentación Completa

Ver [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) para configuración paso a paso.

## 🗄️ Base de Datos

El sistema utiliza Supabase (PostgreSQL) con las siguientes tablas:

- `users_iam` - Usuarios del sistema
- `profiles` - Perfiles de usuario
- `task_templates` - Plantillas de tareas
- `tasks_mind` - Tareas de mente
- `tasks_body` - Tareas de cuerpo
- `achievements` - Logros
- `goals` - Metas
- `task_logs` - Registro de tareas
- `failures` - Registro de fallos
- `bot_rules` - Reglas del bot
- `chat_ia_sessions` - Sesiones de chat
- `chat_ia_messages` - Mensajes de chat

## 🧪 Testing

### Ejemplo con cURL
```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}' \
  | jq -r '.token')

# 2. Obtener perfil
curl -X GET http://localhost:5000/api/profile \
  -H "Authorization: Bearer $TOKEN"

# 3. Obtener tareas
curl -X GET http://localhost:5000/api/tasks/mind \
  -H "Authorization: Bearer $TOKEN"
```

### Ejemplo con Python
```python
import requests

# Login
response = requests.post('http://localhost:5000/login', json={
    'email': 'test@example.com',
    'password': 'test123'
})
token = response.json()['token']

# Headers con token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Obtener perfil
profile = requests.get('http://localhost:5000/api/profile', headers=headers)
print(profile.json())
```

## 🔒 Seguridad

- ✅ JWT con expiración de 24 horas
- ✅ Bcrypt para hashing de passwords
- ✅ Middleware de autenticación en todas las rutas protegidas
- ✅ Validación de ownership (usuarios solo acceden a sus recursos)
- ✅ CORS configurado
- ✅ Secret key configurable por variable de entorno

## 🚧 Desarrollo

### Agregar Nuevo Endpoint

1. **Crear Service** en `services/`
2. **Crear Controller** en `controllers/`
3. **Crear Routes** en `routes/`
4. **Registrar Blueprint** en `app.py`

Ejemplo:
```python
# services/my_service.py
from lib.db import get_supabase

def get_items():
    supabase = get_supabase()
    res = supabase.from_('items').select('*').execute()
    return res.data

# controllers/my_controller.py
from flask import jsonify
from services.my_service import get_items

def get_all_items():
    items = get_items()
    return jsonify(items), 200

# routes/my_routes.py
from flask import Blueprint
from middleware.auth_middleware import token_required
from controllers.my_controller import get_all_items

my_routes = Blueprint('items', __name__, url_prefix='/api/items')

@my_routes.route('/', methods=['GET'])
@token_required
def get_items_route():
    return get_all_items()

# app.py
from routes.my_routes import my_routes
app.register_blueprint(my_routes)
```

## 🤖 Sistema de Tools del Agente IA

El agente IA incluye un sistema extensible de "tools" que le permiten realizar acciones en el sistema:

### Tools Disponibles
- 🧠 **create_mind_task** - Crea tareas mentales (lectura, meditación, etc.)
- 💪 **create_body_task** - Crea tareas físicas (ejercicio, yoga, etc.)
- 📋 **get_user_tasks** - Consulta tareas del usuario
- 📊 **get_user_stats** - Obtiene estadísticas y progreso

### Ejemplo de Uso
```
Usuario: "Me siento estresado"
Agente: "Te recomiendo meditar 10 minutos. ¿Quieres que lo agregue a tus tareas?"
Usuario: "Sí, por favor"
Agente: [Crea la tarea automáticamente] ✅ "Listo! He agregado 
        'Meditación de 10 minutos' a tus tareas."
```

### Agregar Nuevas Tools

Es muy fácil extender el sistema. Ver [tools/QUICKSTART.md](tools/QUICKSTART.md) para una guía paso a paso.

```python
# 1. Crear en tools/my_tool.py
class MyTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_action"
    
    def execute(self, **kwargs):
        # Tu lógica aquí
        return {"success": True, "message": "Done!"}

# 2. Registrar en agent_service.py
tools = [CreateMindTaskTool(), CreateBodyTaskTool(), MyTool()]
```

Ver documentación completa en [AGENT_TOOLS_SUMMARY.md](AGENT_TOOLS_SUMMARY.md).

## 📝 TODO

- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Rate limiting
- [ ] Logging estructurado
- [ ] Caché de queries frecuentes
- [ ] Paginación en listados
- [ ] Búsqueda y filtros avanzados
- [ ] WebSockets para notificaciones en tiempo real
- [x] ✅ Integración con OpenAI para chat IA con function calling

## 👥 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es privado. Todos los derechos reservados.

## 📧 Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.

---

**¡Happy Coding!** 🎉
