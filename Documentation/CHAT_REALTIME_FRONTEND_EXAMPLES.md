# 🎨 Ejemplos de Integración Frontend - Chat Realtime

Este documento contiene ejemplos completos de cómo integrar el chat en tiempo real en diferentes frameworks frontend.

## 📋 Tabla de Contenidos

1. [React + TypeScript](#react--typescript)
2. [Vue 3 + Composition API](#vue-3--composition-api)
3. [Angular](#angular)
4. [Svelte](#svelte)
5. [Next.js](#nextjs)
6. [React Native](#react-native)

---

## React + TypeScript

### Hook personalizado `useChatRealtime`

```typescript
// hooks/useChatRealtime.ts
import { useState, useCallback, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  id?: string;
}

interface UseChatRealtimeReturn {
  messages: Message[];
  currentMessage: string;
  isStreaming: boolean;
  sessionId: string | null;
  createSession: (title?: string) => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  error: string | null;
}

export function useChatRealtime(
  apiUrl: string,
  token: string
): UseChatRealtimeReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const createSession = useCallback(async (title?: string) => {
    try {
      const response = await fetch(`${apiUrl}/chat/realtime/sessions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title })
      });

      if (!response.ok) {
        throw new Error('Error creating session');
      }

      const session = await response.json();
      setSessionId(session.id);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      throw err;
    }
  }, [apiUrl, token]);

  const sendMessage = useCallback(async (content: string) => {
    if (!sessionId || isStreaming) return;

    // Agregar mensaje del usuario
    const userMessage: Message = {
      role: 'user',
      content
    };
    setMessages(prev => [...prev, userMessage]);

    // Preparar streaming
    setCurrentMessage('');
    setIsStreaming(true);
    setError(null);

    // Crear AbortController para poder cancelar
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(
        `${apiUrl}/chat/realtime/sessions/${sessionId}/stream`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ content }),
          signal: abortControllerRef.current.signal
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      const decoder = new TextDecoder();
      let fullContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const events = chunk.split('\n\n').filter(e => e.trim());

        for (const event of events) {
          if (event.startsWith('data: ')) {
            try {
              const data = JSON.parse(event.substring(6));

              switch (data.type) {
                case 'content':
                  fullContent += data.content;
                  setCurrentMessage(fullContent);
                  break;

                case 'done':
                  setMessages(prev => [
                    ...prev,
                    {
                      role: 'assistant',
                      content: data.full_content,
                      id: data.message_id
                    }
                  ]);
                  setCurrentMessage('');
                  break;

                case 'error':
                  throw new Error(data.error);
              }
            } catch (parseError) {
              console.error('Parse error:', parseError);
            }
          }
        }
      }
    } catch (err) {
      if (err instanceof Error && err.name !== 'AbortError') {
        setError(err.message);
      }
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  }, [apiUrl, token, sessionId, isStreaming]);

  return {
    messages,
    currentMessage,
    isStreaming,
    sessionId,
    createSession,
    sendMessage,
    error
  };
}
```

### Componente de Chat

```tsx
// components/ChatRealtime.tsx
import React, { useEffect, useRef, useState } from 'react';
import { useChatRealtime } from '../hooks/useChatRealtime';

interface ChatRealtimeProps {
  apiUrl: string;
  token: string;
}

export const ChatRealtime: React.FC<ChatRealtimeProps> = ({ apiUrl, token }) => {
  const {
    messages,
    currentMessage,
    isStreaming,
    sessionId,
    createSession,
    sendMessage,
    error
  } = useChatRealtime(apiUrl, token);

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Crear sesión al montar
  useEffect(() => {
    createSession('Nueva conversación');
  }, [createSession]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentMessage]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isStreaming) return;

    const message = inputValue;
    setInputValue('');
    await sendMessage(message);
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4 rounded-t-lg">
        <h1 className="text-2xl font-bold">Chat en Tiempo Real</h1>
        {sessionId && (
          <p className="text-sm opacity-75">Sesión: {sessionId.slice(0, 8)}...</p>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-50 p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[75%] rounded-lg p-3 ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white border border-gray-200'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {/* Current streaming message */}
        {currentMessage && (
          <div className="flex justify-start">
            <div className="max-w-[75%] rounded-lg p-3 bg-white border border-gray-200">
              {currentMessage}
              <span className="inline-block w-2 h-4 ml-1 bg-gray-800 animate-pulse" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2">
          Error: {error}
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex gap-2 p-4 bg-white border-t">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Escribe tu mensaje..."
          disabled={isStreaming}
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={isStreaming || !inputValue.trim()}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isStreaming ? 'Enviando...' : 'Enviar'}
        </button>
      </form>
    </div>
  );
};
```

---

## Vue 3 + Composition API

### Composable `useChatRealtime`

```typescript
// composables/useChatRealtime.ts
import { ref, Ref } from 'vue';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  id?: string;
}

export function useChatRealtime(apiUrl: string, token: string) {
  const messages: Ref<Message[]> = ref([]);
  const currentMessage = ref('');
  const isStreaming = ref(false);
  const sessionId = ref<string | null>(null);
  const error = ref<string | null>(null);

  const createSession = async (title?: string) => {
    try {
      const response = await fetch(`${apiUrl}/chat/realtime/sessions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title })
      });

      if (!response.ok) throw new Error('Error creating session');

      const session = await response.json();
      sessionId.value = session.id;
      error.value = null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
      throw err;
    }
  };

  const sendMessage = async (content: string) => {
    if (!sessionId.value || isStreaming.value) return;

    messages.value.push({ role: 'user', content });
    currentMessage.value = '';
    isStreaming.value = true;
    error.value = null;

    try {
      const response = await fetch(
        `${apiUrl}/chat/realtime/sessions/${sessionId.value}/stream`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ content })
        }
      );

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      const decoder = new TextDecoder();
      let fullContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const events = chunk.split('\n\n').filter(e => e.trim());

        for (const event of events) {
          if (event.startsWith('data: ')) {
            const data = JSON.parse(event.substring(6));

            if (data.type === 'content') {
              fullContent += data.content;
              currentMessage.value = fullContent;
            } else if (data.type === 'done') {
              messages.value.push({
                role: 'assistant',
                content: data.full_content,
                id: data.message_id
              });
              currentMessage.value = '';
            } else if (data.type === 'error') {
              throw new Error(data.error);
            }
          }
        }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      isStreaming.value = false;
    }
  };

  return {
    messages,
    currentMessage,
    isStreaming,
    sessionId,
    error,
    createSession,
    sendMessage
  };
}
```

### Componente de Chat

```vue
<!-- components/ChatRealtime.vue -->
<template>
  <div class="chat-container">
    <!-- Header -->
    <div class="chat-header">
      <h1>Chat en Tiempo Real</h1>
      <p v-if="sessionId">Sesión: {{ sessionId.slice(0, 8) }}...</p>
    </div>

    <!-- Messages -->
    <div ref="messagesContainer" class="messages">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.role]"
      >
        {{ msg.content }}
      </div>

      <!-- Streaming message -->
      <div v-if="currentMessage" class="message assistant streaming">
        {{ currentMessage }}
        <span class="cursor">▊</span>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="error">
      Error: {{ error }}
    </div>

    <!-- Input -->
    <form @submit.prevent="handleSubmit" class="input-form">
      <input
        v-model="inputValue"
        type="text"
        placeholder="Escribe tu mensaje..."
        :disabled="isStreaming"
      />
      <button type="submit" :disabled="isStreaming || !inputValue.trim()">
        {{ isStreaming ? 'Enviando...' : 'Enviar' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import { useChatRealtime } from '@/composables/useChatRealtime';

const props = defineProps<{
  apiUrl: string;
  token: string;
}>();

const {
  messages,
  currentMessage,
  isStreaming,
  sessionId,
  error,
  createSession,
  sendMessage
} = useChatRealtime(props.apiUrl, props.token);

const inputValue = ref('');
const messagesContainer = ref<HTMLDivElement>();

onMounted(() => {
  createSession('Nueva conversación');
});

// Auto-scroll
watch([messages, currentMessage], async () => {
  await nextTick();
  messagesContainer.value?.scrollTo({
    top: messagesContainer.value.scrollHeight,
    behavior: 'smooth'
  });
});

const handleSubmit = async () => {
  if (!inputValue.value.trim() || isStreaming.value) return;

  const message = inputValue.value;
  inputValue.value = '';
  await sendMessage(message);
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

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  text-align: center;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f8f9fa;
}

.message {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  max-width: 75%;
}

.message.user {
  background: #667eea;
  color: white;
  margin-left: auto;
}

.message.assistant {
  background: white;
  border: 1px solid #e0e0e0;
}

.message.streaming .cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.error {
  background: #fee;
  color: #c00;
  padding: 0.5rem;
  text-align: center;
}

.input-form {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-form input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
}

.input-form button {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}

.input-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
```

---

## Angular

### Service `ChatRealtimeService`

```typescript
// services/chat-realtime.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  id?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatRealtimeService {
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  private currentMessageSubject = new BehaviorSubject<string>('');
  private isStreamingSubject = new BehaviorSubject<boolean>(false);
  private sessionIdSubject = new BehaviorSubject<string | null>(null);
  private errorSubject = new BehaviorSubject<string | null>(null);

  messages$: Observable<Message[]> = this.messagesSubject.asObservable();
  currentMessage$: Observable<string> = this.currentMessageSubject.asObservable();
  isStreaming$: Observable<boolean> = this.isStreamingSubject.asObservable();
  sessionId$: Observable<string | null> = this.sessionIdSubject.asObservable();
  error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private apiUrl: string, private token: string) {}

  async createSession(title?: string): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/chat/realtime/sessions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title })
      });

      if (!response.ok) throw new Error('Error creating session');

      const session = await response.json();
      this.sessionIdSubject.next(session.id);
      this.errorSubject.next(null);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      this.errorSubject.next(message);
      throw error;
    }
  }

  async sendMessage(content: string): Promise<void> {
    const sessionId = this.sessionIdSubject.value;
    if (!sessionId || this.isStreamingSubject.value) return;

    // Add user message
    const currentMessages = this.messagesSubject.value;
    this.messagesSubject.next([...currentMessages, { role: 'user', content }]);

    this.currentMessageSubject.next('');
    this.isStreamingSubject.next(true);
    this.errorSubject.next(null);

    try {
      const response = await fetch(
        `${this.apiUrl}/chat/realtime/sessions/${sessionId}/stream`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ content })
        }
      );

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      const decoder = new TextDecoder();
      let fullContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const events = chunk.split('\n\n').filter(e => e.trim());

        for (const event of events) {
          if (event.startsWith('data: ')) {
            const data = JSON.parse(event.substring(6));

            if (data.type === 'content') {
              fullContent += data.content;
              this.currentMessageSubject.next(fullContent);
            } else if (data.type === 'done') {
              const messages = this.messagesSubject.value;
              this.messagesSubject.next([
                ...messages,
                {
                  role: 'assistant',
                  content: data.full_content,
                  id: data.message_id
                }
              ]);
              this.currentMessageSubject.next('');
            } else if (data.type === 'error') {
              throw new Error(data.error);
            }
          }
        }
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      this.errorSubject.next(message);
    } finally {
      this.isStreamingSubject.next(false);
    }
  }
}
```

---

## 🎯 Conclusión

Estos ejemplos te permiten integrar el chat en tiempo real en cualquier framework frontend moderno. Todos utilizan la misma API y el mismo formato de eventos SSE.

### Características comunes:

- ✅ Streaming en tiempo real
- ✅ Manejo de errores
- ✅ Auto-scroll automático
- ✅ Estado de carga
- ✅ TypeScript support
- ✅ Responsive design

Adapta estos ejemplos según las necesidades de tu proyecto.
