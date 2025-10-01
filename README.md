# IAM Backend - Sistema de Gestión de Tareas y Bienestar

Backend completo desarrollado en Flask con autenticación JWT, gestión de tareas (mente y cuerpo), perfiles de usuario, logros, metas, chat IA y sistema de bot automatizado.

## 🚀 Características Principales

- ✅ **Autenticación JWT** - Sistema seguro de autenticación con tokens
- ✅ **Gestión de Perfiles** - Perfiles personalizados de usuario
- ✅ **Sistema de Tareas** - Tareas de mente y cuerpo con plantillas reutilizables
- ✅ **Logros y Metas** - Sistema de gamificación y objetivos
- ✅ **Chat IA** - Gestión de sesiones y mensajes de chat
- ✅ **Bot Rules** - Sistema de reglas automáticas configurable
- ✅ **Registro de Actividades** - Logs y tracking de fallos
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
pip install flask flask-cors flasgger supabase pyjwt bcrypt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz:
```env
JWT_SECRET_KEY=tu-secret-key-super-segura-aqui
SUPABASE_URL=tu-supabase-project-url
SUPABASE_KEY=tu-supabase-anon-key
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

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Documentación completa de endpoints
- **[JWT_AUTHENTICATION.md](JWT_AUTHENTICATION.md)** - Guía de autenticación JWT
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Resumen técnico de implementación

## 🏗️ Estructura del Proyecto

```
iam-backend/
├── app.py                    # Aplicación principal
├── middleware/               # Middleware de autenticación
├── services/                 # Lógica de negocio
├── controllers/              # Controladores HTTP
├── routes/                   # Definición de rutas
└── lib/                      # Utilidades (DB, etc.)
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

### Chat IA
- `GET /api/chat/sessions` - Obtener sesiones de chat
- `POST /api/chat/sessions` - Crear sesión
- `GET /api/chat/sessions/<id>/messages` - Obtener mensajes

Ver documentación completa en [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

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

## 📝 TODO

- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Rate limiting
- [ ] Logging estructurado
- [ ] Caché de queries frecuentes
- [ ] Paginación en listados
- [ ] Búsqueda y filtros avanzados
- [ ] WebSockets para notificaciones en tiempo real
- [ ] Integración con servicio de LLM para chat IA

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
