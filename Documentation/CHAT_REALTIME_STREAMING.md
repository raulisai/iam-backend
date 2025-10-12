# Chat en Tiempo Real (Realtime Chat)

Sistema de chat streaming similar a ChatGPT que permite conversaciones fluidas en tiempo real.

## 🚀 Características

- **Streaming en tiempo real**: Las respuestas se van mostrando palabra por palabra como en ChatGPT
- **Server-Sent Events (SSE)**: Tecnología estándar para streaming del servidor al cliente
- **Sin bloqueos**: El usuario puede ver la respuesta mientras se está generando
- **Historial de conversación**: Mantiene el contexto de la conversación completa
- **Compatibilidad**: No requiere la ruta anterior de `chat_ia_realtime`

## 📍 Endpoints

### 1. Crear Sesión de Chat

```
POST /api/chat/realtime/sessions
```

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
Content-Type: application/json
```

**Body (opcional):**
```json
{
  "title": "Mi conversación",
  "initial_message": "Hola, ¿cómo puedo mejorar mi productividad?"
}
```

**Respuesta:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Mi conversación",
  "created_at": "2025-10-11T10:30:00.000Z",
  "updated_at": "2025-10-11T10:30:00.000Z"
}
```

### 2. Enviar Mensaje y Recibir Streaming

```
POST /api/chat/realtime/sessions/{session_id}/stream
```

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
Content-Type: application/json
```

**Body:**
```json
{
  "content": "¿Cómo puedo ser más productivo?"
}
```

**Respuesta (Server-Sent Events):**

El servidor responde con un stream de eventos en formato SSE:

```
data: {"type": "start", "session_id": "550e8400-e29b-41d4-a716-446655440000"}

data: {"type": "content", "content": "Para"}

data: {"type": "content", "content": " mejorar"}

data: {"type": "content", "content": " tu"}

data: {"type": "content", "content": " productividad"}

data: {"type": "content", "content": "..."}

data: {"type": "done", "message_id": "msg-123", "full_content": "Para mejorar tu productividad..."}
```

## 💻 Ejemplo de Integración Frontend

### Usando JavaScript Vanilla

```javascript
// Crear una sesión
async function createChatSession() {
  const response = await fetch('http://localhost:5000/api/chat/realtime/sessions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: 'Nueva conversación'
    })
  });
  
  return await response.json();
}

// Enviar mensaje con streaming
function sendStreamingMessage(sessionId, message) {
  const eventSource = new EventSource(
    `http://localhost:5000/api/chat/realtime/sessions/${sessionId}/stream`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  // En realidad, EventSource no soporta POST directamente
  // Usa fetch con streaming manual:
  
  fetch(`http://localhost:5000/api/chat/realtime/sessions/${sessionId}/stream`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: message })
  })
  .then(response => {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    function readStream() {
      reader.read().then(({ done, value }) => {
        if (done) {
          console.log('Stream terminado');
          return;
        }
        
        // Decodificar el chunk
        const chunk = decoder.decode(value, { stream: true });
        
        // Procesar cada evento SSE
        const events = chunk.split('\n\n');
        events.forEach(event => {
          if (event.startsWith('data: ')) {
            const data = JSON.parse(event.substring(6));
            
            switch(data.type) {
              case 'start':
                console.log('Iniciando respuesta...');
                break;
              case 'content':
                // Agregar contenido al UI
                appendToMessage(data.content);
                break;
              case 'done':
                console.log('Respuesta completa:', data.full_content);
                break;
              case 'error':
                console.error('Error:', data.error);
                break;
            }
          }
        });
        
        // Continuar leyendo
        readStream();
      });
    }
    
    readStream();
  });
}

// Función auxiliar para agregar contenido al mensaje
function appendToMessage(content) {
  const messageElement = document.getElementById('current-message');
  messageElement.textContent += content;
}
```

### Usando React

```jsx
import { useState, useEffect } from 'react';

function ChatRealtime() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  // Crear sesión al montar
  useEffect(() => {
    createSession();
  }, []);

  async function createSession() {
    const response = await fetch('/api/chat/realtime/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title: 'Nueva conversación' })
    });
    
    const session = await response.json();
    setSessionId(session.id);
  }

  async function sendMessage() {
    if (!inputValue.trim() || !sessionId || isStreaming) return;

    const userMessage = inputValue;
    setInputValue('');
    
    // Agregar mensaje del usuario
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    // Preparar mensaje del asistente
    setCurrentMessage('');
    setIsStreaming(true);

    try {
      const response = await fetch(
        `/api/chat/realtime/sessions/${sessionId}/stream`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ content: userMessage })
        }
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const events = chunk.split('\n\n');

        for (const event of events) {
          if (event.startsWith('data: ')) {
            const data = JSON.parse(event.substring(6));

            if (data.type === 'content') {
              fullContent += data.content;
              setCurrentMessage(fullContent);
            } else if (data.type === 'done') {
              setMessages(prev => [
                ...prev,
                { role: 'assistant', content: data.full_content }
              ]);
              setCurrentMessage('');
            } else if (data.type === 'error') {
              console.error('Error:', data.error);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error al enviar mensaje:', error);
    } finally {
      setIsStreaming(false);
    }
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {currentMessage && (
          <div className="message assistant streaming">
            {currentMessage}
            <span className="cursor">▊</span>
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Escribe tu mensaje..."
          disabled={isStreaming}
        />
        <button onClick={sendMessage} disabled={isStreaming}>
          {isStreaming ? 'Enviando...' : 'Enviar'}
        </button>
      </div>
    </div>
  );
}

export default ChatRealtime;
```

### Usando Vue.js

```vue
<template>
  <div class="chat-container">
    <div class="messages">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.role]"
      >
        {{ msg.content }}
      </div>
      <div v-if="currentMessage" class="message assistant streaming">
        {{ currentMessage }}
        <span class="cursor">▊</span>
      </div>
    </div>

    <div class="input-container">
      <input
        v-model="inputValue"
        @keypress.enter="sendMessage"
        placeholder="Escribe tu mensaje..."
        :disabled="isStreaming"
      />
      <button @click="sendMessage" :disabled="isStreaming">
        {{ isStreaming ? 'Enviando...' : 'Enviar' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sessionId: null,
      messages: [],
      currentMessage: '',
      inputValue: '',
      isStreaming: false,
      token: localStorage.getItem('token')
    };
  },
  
  mounted() {
    this.createSession();
  },
  
  methods: {
    async createSession() {
      const response = await fetch('/api/chat/realtime/sessions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: 'Nueva conversación' })
      });
      
      const session = await response.json();
      this.sessionId = session.id;
    },
    
    async sendMessage() {
      if (!this.inputValue.trim() || !this.sessionId || this.isStreaming) {
        return;
      }

      const userMessage = this.inputValue;
      this.inputValue = '';
      
      // Agregar mensaje del usuario
      this.messages.push({ role: 'user', content: userMessage });
      
      // Preparar mensaje del asistente
      this.currentMessage = '';
      this.isStreaming = true;

      try {
        const response = await fetch(
          `/api/chat/realtime/sessions/${this.sessionId}/stream`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: userMessage })
          }
        );

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const events = chunk.split('\n\n');

          for (const event of events) {
            if (event.startsWith('data: ')) {
              const data = JSON.parse(event.substring(6));

              if (data.type === 'content') {
                fullContent += data.content;
                this.currentMessage = fullContent;
              } else if (data.type === 'done') {
                this.messages.push({
                  role: 'assistant',
                  content: data.full_content
                });
                this.currentMessage = '';
              } else if (data.type === 'error') {
                console.error('Error:', data.error);
              }
            }
          }
        }
      } catch (error) {
        console.error('Error al enviar mensaje:', error);
      } finally {
        this.isStreaming = false;
      }
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 15px;
  padding: 10px 15px;
  border-radius: 10px;
  max-width: 70%;
}

.message.user {
  background-color: #007bff;
  color: white;
  margin-left: auto;
  text-align: right;
}

.message.assistant {
  background-color: #f1f1f1;
  color: #333;
}

.message.streaming .cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.input-container {
  display: flex;
  padding: 20px;
  border-top: 1px solid #ddd;
}

.input-container input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-right: 10px;
}

.input-container button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.input-container button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
```

## 🔧 Curl Examples

### Crear sesión
```bash
curl -X POST http://localhost:5000/api/chat/realtime/sessions \
  -H "Authorization: Bearer tu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Conversación de prueba"
  }'
```

### Enviar mensaje con streaming
```bash
curl -N -X POST http://localhost:5000/api/chat/realtime/sessions/SESSION_ID/stream \
  -H "Authorization: Bearer tu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "¿Cómo puedo mejorar mi productividad?"
  }'
```

**Nota:** La opción `-N` es importante para deshabilitar el buffering y ver el streaming en tiempo real.

## 📊 Formato de Eventos SSE

### Evento: start
```json
{
  "type": "start",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Evento: content
```json
{
  "type": "content",
  "content": "pedazo de texto"
}
```

### Evento: done
```json
{
  "type": "done",
  "message_id": "msg-123",
  "full_content": "respuesta completa"
}
```

### Evento: error
```json
{
  "type": "error",
  "error": "descripción del error"
}
```

## 🔐 Autenticación

Todos los endpoints requieren un token JWT válido en el header `Authorization`:

```
Authorization: Bearer <tu_token_jwt>
```

## 🎯 Casos de Uso

1. **Chat de soporte en tiempo real**
2. **Asistente personal con IA**
3. **Tutor virtual interactivo**
4. **Conversaciones sobre productividad y tareas**
5. **Análisis y recomendaciones en tiempo real**

## ⚠️ Notas Importantes

- **No mover la ruta anterior**: La ruta `/api/chat` (sin `/realtime`) sigue funcionando de forma independiente
- **Streaming requiere OpenAI API Key**: Asegúrate de tener configurada la variable `OPENAI_API_KEY`
- **Modelo usado**: `gpt-4o-mini` (puedes cambiarlo en el controlador)
- **Límite de tokens**: 2000 tokens por respuesta
- **Historial**: Se mantienen los últimos 10 mensajes como contexto

## 🐛 Troubleshooting

### Error: "Session not found"
- Verifica que el `session_id` sea correcto
- Asegúrate de que la sesión pertenezca al usuario autenticado

### Error: "Unauthorized"
- Verifica que el token JWT sea válido
- Asegúrate de incluir el prefijo "Bearer " en el header

### El streaming no funciona
- Verifica que tu frontend esté procesando correctamente el stream
- Asegúrate de que el servidor no tenga proxy/buffering habilitado
- Usa la opción `-N` en curl para testing

### Respuestas lentas
- Verifica tu conexión a internet
- Revisa la configuración de OpenAI
- Considera ajustar el `max_tokens` para respuestas más cortas

## 📚 Recursos Adicionales

- [Server-Sent Events MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [OpenAI Streaming](https://platform.openai.com/docs/api-reference/streaming)
- [Fetch API Streaming](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)
