# Guía de Configuración - Sistema de Automatización

Esta guía te ayudará a configurar el sistema de automatización con GitHub Actions.

## 📋 Prerequisitos

1. Repositorio en GitHub
2. Cuenta de Supabase con base de datos configurada
3. Proyecto de Firebase con FCM habilitado
4. Secrets configurados en GitHub

## 🔧 Paso 1: Configurar Secrets en GitHub

Ve a tu repositorio → Settings → Secrets and variables → Actions → New repository secret

Agrega los siguientes secrets:

### SUPABASE_URL
```
https://tu-proyecto.supabase.co
```

### SUPABASE_SERVICE_ROLE_KEY
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
*Obtén este valor de: Supabase Dashboard → Settings → API → service_role key*

### FIREBASE_SERVICE_ACCOUNT
```json
{
  "type": "service_account",
  "project_id": "tu-proyecto",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-...@tu-proyecto.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```
*Obtén este archivo de: Firebase Console → Project Settings → Service Accounts → Generate new private key*

### JWT_SECRET_KEY
```
tu-secret-key-super-segura-aqui
```
*Genera una clave segura con: `openssl rand -hex 32`*

## 🗄️ Paso 2: Verificar Esquema de Base de Datos

Asegúrate de que las siguientes tablas existan en Supabase:

### Tablas Requeridas

- ✅ `users_iam` - Usuarios
- ✅ `profiles` - Perfiles con timezone
- ✅ `tasks_body` - Tareas físicas
- ✅ `tasks_mind` - Tareas mentales
- ✅ `routine_alarms` - Alarmas de rutina
- ✅ `routine_reminders` - Recordatorios de rutina
- ✅ `performance_snapshots` - Snapshots de rendimiento
- ✅ `device_tokens` - Tokens FCM

### Verificar Tabla performance_snapshots

Si no existe, créala con:

```sql
CREATE TABLE IF NOT EXISTS public.performance_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  snapshot_date DATE NOT NULL,
  metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, snapshot_date)
);

CREATE INDEX IF NOT EXISTS idx_snapshots_user_id ON public.performance_snapshots(user_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_date ON public.performance_snapshots(snapshot_date);
```

## 🚀 Paso 3: Activar GitHub Actions

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Si está deshabilitado, habilita GitHub Actions
4. El workflow `hourly_automation.yml` aparecerá en la lista

## ✅ Paso 4: Probar la Configuración

### Prueba Manual

1. Ve a Actions → Hourly Automation Tasks
2. Click en "Run workflow"
3. Selecciona "metrics" (tarea simple para probar)
4. Click en "Run workflow"
5. Espera a que termine y revisa los logs

### Verificar Logs

Los logs deben mostrar algo como:

```
######################################################################
# IAM Backend Automation Script
# Started at: 2024-10-16 17:00:00
######################################################################

Running specific task: metrics

[MANUAL RUN] Executing task: metrics
[2024-10-16 17:00:01] Starting metrics update...
Updating metrics for 5 users
Completed metrics update for 5 users
Task metrics completed successfully

======================================================================
EXECUTION SUMMARY
======================================================================
✓ Status: success
======================================================================
```

## 🔍 Paso 5: Verificar Datos en Supabase

Después de ejecutar el workflow, verifica en Supabase:

```sql
-- Ver snapshots creados
SELECT * FROM performance_snapshots 
ORDER BY created_at DESC 
LIMIT 10;

-- Ver métricas de un usuario específico
SELECT 
  snapshot_date,
  metrics->>'completed_body_tasks' as body_tasks,
  metrics->>'completed_mind_tasks' as mind_tasks,
  metrics->>'score_body' as body_score,
  metrics->>'score_mind' as mind_score
FROM performance_snapshots
WHERE user_id = 'tu-user-id'
ORDER BY snapshot_date DESC;
```

## 📅 Paso 6: Configurar Horarios (Opcional)

El workflow está configurado para ejecutarse cada hora. Si quieres cambiar la frecuencia:

Edita `.github/workflows/hourly_automation.yml`:

```yaml
on:
  schedule:
    # Cada hora (actual)
    - cron: '0 * * * *'
    
    # Cada 30 minutos
    # - cron: '*/30 * * * *'
    
    # Cada 2 horas
    # - cron: '0 */2 * * *'
    
    # Solo a las 9 AM, 3 PM y 11 PM
    # - cron: '0 9,15,23 * * *'
```

## 🧪 Paso 7: Pruebas Locales (Opcional)

Para probar localmente antes de hacer push:

```bash
# 1. Clonar el repositorio
git clone tu-repo.git
cd iam-backend

# 2. Crear archivo .env
cat > .env << EOF
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
FIREBASE_SERVICE_ACCOUNT=./firebase-credentials.json
JWT_SECRET_KEY=tu-secret-key
EOF

# 3. Descargar credenciales de Firebase
# Coloca el archivo JSON en la raíz como firebase-credentials.json

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar script
python scripts/run_automation.py metrics
```

## 📊 Monitoreo

### Ver Ejecuciones Pasadas

1. Ve a Actions → Hourly Automation Tasks
2. Verás todas las ejecuciones con su estado (✓ o ✗)
3. Click en cualquiera para ver logs detallados

### Configurar Notificaciones de Errores

GitHub puede enviarte emails si un workflow falla:

1. Ve a tu perfil → Settings → Notifications
2. En "Actions", marca "Send notifications for failed workflows"

## 🐛 Troubleshooting

### Error: "Module not found"

**Solución:** Verifica que `requirements.txt` incluya todas las dependencias:

```txt
flask==3.0.0
supabase==2.10.0
firebase-admin==6.5.0
pytz==2024.1
python-dotenv==1.0.0
```

### Error: "Supabase connection failed"

**Solución:** Verifica que los secrets `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` estén correctos.

### Error: "Firebase not initialized"

**Solución:** Verifica que `FIREBASE_SERVICE_ACCOUNT` sea un JSON válido.

### No se envían notificaciones

**Posibles causas:**
1. No hay tokens FCM registrados en `device_tokens`
2. Los tokens están inactivos (`is_active = false`)
3. Las alarmas/recordatorios no están activos (`is_active = false`)
4. El día actual no está en `days_of_week`

**Verificar:**
```sql
-- Ver tokens activos
SELECT * FROM device_tokens WHERE is_active = true;

-- Ver alarmas activas
SELECT * FROM routine_alarms WHERE is_active = true;
```

### Scores no se actualizan

**Verificar:**
1. Que el workflow se ejecute a las 23:00 (11 PM)
2. Que existan tareas pendientes para el día
3. Que los usuarios tengan timezone configurado en `profiles`

```sql
-- Ver perfiles con timezone
SELECT user_id, timezone FROM profiles;
```

## 📝 Checklist Final

- [ ] Todos los secrets configurados en GitHub
- [ ] Tablas de base de datos creadas
- [ ] GitHub Actions habilitado
- [ ] Prueba manual exitosa
- [ ] Datos verificados en Supabase
- [ ] Notificaciones de errores configuradas

## 🎉 ¡Listo!

Tu sistema de automatización está configurado y funcionando. El workflow se ejecutará automáticamente cada hora y:

- ✅ Enviará notificaciones programadas
- ✅ Actualizará métricas de usuarios
- ✅ Calculará scores al final del día (23:00)
- ✅ Limpiará datos antiguos semanalmente

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs en GitHub Actions
2. Verifica los secrets
3. Consulta el archivo `automation/README.md` para más detalles
4. Ejecuta pruebas locales para debugging
