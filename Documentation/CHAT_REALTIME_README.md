# 💬 Chat en Tiempo Real - Guía Rápida

## 🚀 Inicio Rápido (5 minutos)

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
# .env
OPENAI_API_KEY=tu_api_key
JWT_SECRET_KEY=tu_secret
SUPABASE_URL=tu_url
SUPABASE_KEY=tu_key
```

### 3. Iniciar el Servidor
```bash
python app.py
```

### 4. Probar con la Demo
Abre `test/chat_realtime_demo.html` en tu navegador

---

## 📍 Endpoints Principales

### Crear Sesión
```bash
POST /api/chat/realtime/sessions
Authorization: Bearer TOKEN

{
  "title": "Mi conversación"
}
```

### Enviar Mensaje con Streaming
```bash
POST /api/chat/realtime/sessions/{session_id}/stream
Authorization: Bearer TOKEN

{
  "content": "Hola, ¿cómo estás?"
}
```

Respuesta: Stream de eventos SSE
```
data: {"type": "start", "session_id": "..."}
data: {"type": "content", "content": "Hola"}
data: {"type": "content", "content": ", ¿qué"}
data: {"type": "done", "message_id": "...", "full_content": "..."}
```

---

## 💻 Ejemplo Frontend (JavaScript)

```javascript
// 1. Crear sesión
const session = await fetch('/api/chat/realtime/sessions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
}).then(r => r.json());

// 2. Enviar mensaje con streaming
const response = await fetch(
  `/api/chat/realtime/sessions/${session.id}/stream`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: 'Hola' })
  }
);

// 3. Leer stream
const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value, { stream: true });
  const events = chunk.split('\n\n');

  for (const event of events) {
    if (event.startsWith('data: ')) {
      const data = JSON.parse(event.substring(6));
      
      if (data.type === 'content') {
        // Mostrar contenido en tiempo real
        console.log(data.content);
      } else if (data.type === 'done') {
        // Streaming completado
        console.log('Done!', data.full_content);
      }
    }
  }
}
```

---

## 📚 Documentación Completa

- **[Implementación Completa](CHAT_REALTIME_IMPLEMENTATION_SUMMARY.md)** - Resumen de todo lo implementado
- **[Guía de Streaming](CHAT_REALTIME_STREAMING.md)** - Documentación técnica detallada
- **[Ejemplos Frontend](CHAT_REALTIME_FRONTEND_EXAMPLES.md)** - React, Vue, Angular, etc.

---

## 🎯 Características

✅ **Streaming en tiempo real** - Como ChatGPT  
✅ **Server-Sent Events** - Tecnología estándar  
✅ **Sin bloqueos** - Respuestas fluidas  
✅ **Historial de conversación** - Contexto automático  
✅ **Autenticación JWT** - Seguro  
✅ **Integración OpenAI** - IA potente  

---

## 🧪 Testing

### Con Python
```bash
cd test
python test_chat_realtime.py
```

### Con curl
```bash
# Streaming visible con -N
curl -N -X POST http://localhost:5000/api/chat/realtime/sessions/SESSION_ID/stream \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hola"}'
```

### Con HTML
```bash
# Abrir en navegador
test/chat_realtime_demo.html
```

---

## ⚠️ Nota Importante

**La ruta anterior `/api/chat` NO se ha movido ni modificado.**  

Ahora tienes dos opciones:
- `/api/chat` - Chat normal (respuesta completa al final)
- `/api/chat/realtime` - Chat con streaming (respuesta en tiempo real)

Usa el que mejor se adapte a tu caso de uso.

---

## 🆘 Problemas Comunes

**El streaming no se ve**: Usa `-N` en curl o deshabilita buffering  
**Error 401**: Verifica tu token JWT  
**Error 404**: Asegúrate de que el servidor esté corriendo  
**Respuestas lentas**: Verifica tu API key de OpenAI  

---

## 📞 Soporte

Para más información, revisa la documentación completa en el directorio `Documentation/`.

¡Disfruta del chat en tiempo real! 🎉
