# ✅ Checklist de Despliegue en Render

## Antes de Desplegar

- [ ] **Git Status Limpio**
  ```bash
  git status
  ```

- [ ] **Variables de Entorno Locales Funcionando**
  - [ ] `JWT_SECRET_KEY` configurado
  - [ ] `SUPABASE_URL` configurado
  - [ ] `SUPABASE_KEY` configurado
  - [ ] `OPENAI_API_KEY` configurado

- [ ] **API Funciona Localmente**
  ```bash
  python app.py
  # Visita: http://localhost:5000/apidocs/
  ```

- [ ] **Dependencias Actualizadas**
  - [ ] Verificar `requirements.txt` está completo
  - [ ] Incluye `gunicorn==21.2.0`

## Archivos de Configuración Creados ✅

- [x] `render.yaml` - Configuración de Render
- [x] `Procfile` - Comando de inicio alternativo
- [x] `runtime.txt` - Versión de Python
- [x] `.python-version` - Versión de Python para pyenv
- [x] `gunicorn_config.py` - Configuración de Gunicorn
- [x] `.renderignore` - Archivos a ignorar en deploy
- [x] `.env.example` - Template de variables de entorno
- [x] `DEPLOYMENT_GUIDE.md` - Guía completa
- [x] `RENDER_QUICKSTART.md` - Guía rápida

## Cambios en Código ✅

- [x] `app.py` actualizado con:
  - [x] Puerto dinámico (`PORT` env var)
  - [x] CORS configurado para producción
  - [x] Debug mode condicional
  - [x] Host `0.0.0.0` para Render

## Durante el Despliegue en Render

### 1. Preparar GitHub
- [ ] Commit de todos los cambios
  ```bash
  git add .
  git commit -m "Preparar para despliegue en Render"
  git push origin master
  ```

### 2. Crear Web Service en Render
- [ ] Ir a https://dashboard.render.com
- [ ] Click "New +" → "Web Service"
- [ ] Conectar repositorio GitHub
- [ ] Seleccionar `iam-backend`

### 3. Configuración Automática (Render.yaml)
- [ ] Render detecta `render.yaml`
- [ ] Verifica que la configuración sea correcta:
  - Runtime: Python 3
  - Build: `pip install -r requirements.txt`
  - Start: `gunicorn app:app`
  - Plan: Free

### 4. Variables de Entorno
Configurar en Render Dashboard → Environment:

**Requeridas:**
- [ ] `SUPABASE_URL` = `https://xxxxx.supabase.co`
- [ ] `SUPABASE_KEY` = `eyJxxx...`
- [ ] `OPENAI_API_KEY` = `sk-xxxxx`
- [ ] `FRONTEND_URL` = `https://tu-frontend.vercel.app`

**Automáticas (render.yaml):**
- [x] `PYTHON_VERSION` = `3.11.0`
- [x] `FLASK_ENV` = `production`
- [x] `JWT_SECRET_KEY` = (auto-generado)

### 5. Deploy
- [ ] Click "Create Web Service"
- [ ] Esperar build (2-5 minutos)
- [ ] Verificar logs sin errores

## Después del Despliegue

### Verificación
- [ ] **API Responde**
  ```bash
  curl https://iam-backend.onrender.com/apidocs/
  ```

- [ ] **Swagger UI Accesible**
  - Abrir: `https://iam-backend.onrender.com/apidocs/`

- [ ] **Endpoints Funcionan**
  - [ ] POST `/auth/signup`
  - [ ] POST `/auth/login`
  - [ ] GET `/tasks` (con token)

- [ ] **CORS Configurado**
  - Prueba desde tu frontend
  - Verifica que no hay errores de CORS

### Configurar Frontend
- [ ] Actualizar URL del backend en frontend:
  ```javascript
  const API_URL = 'https://iam-backend.onrender.com';
  ```

- [ ] Agregar URL del frontend a `FRONTEND_URL` en Render
- [ ] Verificar peticiones desde frontend funcionan

### Opcional: Evitar Cold Start
- [ ] Configurar UptimeRobot:
  1. Ir a https://uptimerobot.com
  2. Crear monitor HTTP(S)
  3. URL: `https://iam-backend.onrender.com/apidocs/`
  4. Intervalo: 5 minutos

## Troubleshooting

### ❌ Build Falla
- [ ] Verificar `requirements.txt` tiene todas las dependencias
- [ ] Revisar logs de build en Render
- [ ] Verificar versión de Python correcta

### ❌ Application Failed to Respond
- [ ] Verificar `gunicorn` está en requirements.txt
- [ ] Revisar logs de runtime
- [ ] Verificar `PORT` env var está siendo usada

### ❌ Errores de Importación
- [ ] Verificar estructura de carpetas
- [ ] Verificar `__init__.py` en todas las carpetas de módulos
- [ ] Revisar imports relativos vs absolutos

### ❌ Errores de CORS
- [ ] Verificar `FRONTEND_URL` configurada correctamente
- [ ] Revisar que el origen del request está en la lista permitida
- [ ] Verificar headers en la petición

### ❌ Errores de Base de Datos
- [ ] Verificar `SUPABASE_URL` correcta
- [ ] Verificar `SUPABASE_KEY` correcta
- [ ] Probar conexión manualmente

### ❌ Errores de OpenAI
- [ ] Verificar `OPENAI_API_KEY` válida
- [ ] Verificar límites de uso de OpenAI
- [ ] Revisar logs de errores específicos

## Monitoreo Continuo

### Logs
- [ ] Configurar alertas en Render
- [ ] Revisar logs regularmente
  ```
  Dashboard → Logs (en tiempo real)
  ```

### Rendimiento
- [ ] Monitorear tiempos de respuesta
- [ ] Verificar cold starts
- [ ] Considerar upgrade a plan pagado si es necesario

### Actualizaciones
- [ ] Deploy automático configurado (GitHub → Render)
- [ ] Probar cambios en local antes de push
- [ ] Revisar logs después de cada deploy

## 🎉 ¡Despliegue Completo!

Tu API está en producción:
- **URL Base**: `https://iam-backend.onrender.com`
- **Swagger UI**: `https://iam-backend.onrender.com/apidocs/`
- **Status**: Render Dashboard

---

## 📞 Soporte

- [Render Docs](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Status Page](https://status.render.com)

## 📝 Notas Adicionales

**Capa Gratuita:**
- 750 horas/mes (suficiente para proyectos personales)
- Se suspende después de 15 minutos sin actividad
- Cold start de ~50 segundos en primera petición
- 512 MB RAM

**Plan Pagado ($7/mes):**
- Sin suspensión
- Sin cold starts
- Más RAM
- Mejor para producción seria

---

**Fecha de Despliegue**: _____________

**URL de Producción**: _____________

**Notas**: 
_____________________________________________
_____________________________________________
_____________________________________________
