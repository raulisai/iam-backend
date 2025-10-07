# 🚀 Guía de Despliegue en Render

Este documento describe cómo desplegar el proyecto IAM Backend en Render.com usando su capa gratuita.

## 📋 Pre-requisitos

1. Cuenta en [Render.com](https://render.com) (gratuita)
2. Repositorio en GitHub con el código actualizado
3. Variables de entorno necesarias:
   - `JWT_SECRET_KEY` - Clave secreta para JWT (se genera automáticamente)
   - `SUPABASE_URL` - URL de tu proyecto Supabase
   - `SUPABASE_KEY` - API Key de Supabase
   - `OPENAI_API_KEY` - API Key de OpenAI
   - `FRONTEND_URL` - URL de tu frontend en producción (opcional)

## 🔧 Archivos de Configuración

El proyecto ya incluye todos los archivos necesarios:

- ✅ `requirements.txt` - Dependencias de Python
- ✅ `render.yaml` - Configuración de Render (Blueprint)
- ✅ `runtime.txt` - Versión de Python
- ✅ `.python-version` - Versión de Python para pyenv
- ✅ `app.py` - Configurado para producción

## 📝 Pasos para Desplegar

### 1. Preparar el Repositorio

```bash
# Asegúrate de que todos los cambios estén commiteados
git add .
git commit -m "Preparar para despliegue en Render"
git push origin master
```

### 2. Crear el Web Service en Render

#### Opción A: Usando Blueprint (Recomendado)

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New +"** → **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Click en **"Apply"**
6. Ve a **"Environment"** y configura las variables de entorno:
   - `SUPABASE_URL`: Tu URL de Supabase
   - `SUPABASE_KEY`: Tu API Key de Supabase
   - `OPENAI_API_KEY`: Tu API Key de OpenAI
   - `FRONTEND_URL`: URL de tu frontend (ej: `https://tu-app.vercel.app`)

#### Opción B: Configuración Manual

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: `iam-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`
5. Click en **"Advanced"** y agrega las variables de entorno:
   - `PYTHON_VERSION`: `3.11.0`
   - `JWT_SECRET_KEY`: (genera uno seguro o déjalo autogenerar)
   - `SUPABASE_URL`: Tu URL
   - `SUPABASE_KEY`: Tu Key
   - `OPENAI_API_KEY`: Tu Key
   - `FLASK_ENV`: `production`
   - `FRONTEND_URL`: URL de tu frontend
6. Click en **"Create Web Service"**

### 3. Verificar el Despliegue

Una vez que el servicio esté desplegado:

1. Render te dará una URL como: `https://iam-backend.onrender.com`
2. Verifica que la API funcione:
   - Swagger UI: `https://iam-backend.onrender.com/apidocs/`
   - Health check: `https://iam-backend.onrender.com/`

### 4. Configurar el Frontend

Actualiza tu frontend para usar la nueva URL del backend:

```javascript
// En tu archivo de configuración del frontend
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://iam-backend.onrender.com'
  : 'http://localhost:5000';
```

## ⚠️ Consideraciones Importantes

### Capa Gratuita de Render

- ✅ **750 horas/mes** de uso (suficiente para proyectos personales)
- ⚠️ **Se suspende después de 15 minutos de inactividad**
- ⏱️ **Primera petición puede tardar 50+ segundos** (cold start)
- 💾 **512 MB de RAM**
- 🌐 **SSL automático** incluido

### Optimizaciones

Para evitar el cold start en tu aplicación:

1. **Usar un servicio de ping** (opcional):
   - [UptimeRobot](https://uptimerobot.com) - Pinga tu URL cada 5 minutos
   - [Cron-job.org](https://cron-job.org) - Scheduler gratuito

2. **Actualizar a plan pagado** ($7/mes):
   - Sin suspensión
   - Más recursos
   - Sin cold starts

### Logs y Monitoreo

```bash
# Ver logs en tiempo real desde el dashboard de Render
# O usando la CLI:
render logs -t iam-backend
```

## 🔐 Seguridad

1. **JWT_SECRET_KEY**: Usa una clave fuerte y única
   ```bash
   # Genera una clave segura:
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Variables de Entorno**: Nunca las subas al repositorio
3. **CORS**: Ya configurado para tu frontend específico

## 🔄 Actualizar el Despliegue

Render se actualiza automáticamente cuando haces push a GitHub:

```bash
git add .
git commit -m "Actualización"
git push origin master
# Render detecta el cambio y redespliega automáticamente
```

## 🐛 Troubleshooting

### Error: "Application failed to respond"

**Solución**: Verifica que gunicorn esté en `requirements.txt` y que el comando de inicio sea correcto.

### Error: "Module not found"

**Solución**: 
```bash
# Asegúrate de que todas las dependencias estén en requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Actualizar dependencias"
git push
```

### Error de CORS

**Solución**: Agrega la URL correcta de tu frontend en la variable `FRONTEND_URL`.

### Cold Start muy lento

**Solución**: Considera usar UptimeRobot para mantener el servicio activo o actualizar a plan pagado.

## 📚 Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Render Status](https://status.render.com)
- [Render Community](https://community.render.com)
- [Guía de Flask en Render](https://render.com/docs/deploy-flask)

## 🆘 Soporte

Si encuentras problemas:

1. Revisa los logs en el dashboard de Render
2. Verifica que todas las variables de entorno estén configuradas
3. Consulta la documentación de Render
4. Abre un issue en el repositorio

---

**¡Tu API está lista para producción! 🎉**

URL de tu API: `https://iam-backend.onrender.com`
Swagger UI: `https://iam-backend.onrender.com/apidocs/`
