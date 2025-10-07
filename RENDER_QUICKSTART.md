# 🚀 Despliegue Rápido en Render

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Sube tu código a GitHub
```bash
git add .
git commit -m "Preparar para despliegue en Render"
git push origin master
```

### 2️⃣ Crea el servicio en Render
1. Ve a https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Conecta tu repo: `raulisai/iam-backend`
4. Render detectará automáticamente la configuración ✨

### 3️⃣ Configura Variables de Entorno
En el dashboard de Render, agrega:
- ✅ `SUPABASE_URL` → Tu URL de Supabase
- ✅ `SUPABASE_KEY` → Tu API Key
- ✅ `OPENAI_API_KEY` → Tu API Key de OpenAI
- ✅ `FRONTEND_URL` → URL de tu frontend
- ✅ `JWT_SECRET_KEY` → Se genera automático (o usa el tuyo)

### 4️⃣ ¡Deploy!
Click **"Create Web Service"** y espera 2-3 minutos 🎉

---

## 🔗 Tu API estará en:
```
https://iam-backend.onrender.com
```

## 📖 Swagger UI:
```
https://iam-backend.onrender.com/apidocs/
```

---

## ⚠️ Importante: Capa Gratuita
- Primera petición tarda ~50 segundos (cold start)
- Se suspende después de 15 minutos sin uso
- 750 horas/mes incluidas (suficiente para uso personal)

## 💡 Solución para Cold Start
Usa [UptimeRobot](https://uptimerobot.com) gratis para hacer ping cada 5 minutos.

---

## 📚 Documentación Completa
Lee `DEPLOYMENT_GUIDE.md` para más detalles.

## 🆘 Problemas?
1. Revisa los logs en Render dashboard
2. Verifica las variables de entorno
3. Consulta `DEPLOYMENT_GUIDE.md`
