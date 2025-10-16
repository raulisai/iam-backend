# Snapshot Update Latest - Ejemplos de Uso

## Descripción

El endpoint `/api/stats/snapshots/update-latest` (método POST) actualiza el snapshot más reciente del usuario autenticado con datos crudos de salud.

**Características:**
- Solo actualiza los campos que NO son `null`
- Los campos `null` se ignoran y mantienen su valor anterior
- Si no existe un snapshot previo, crea uno nuevo
- Procesa y formatea automáticamente los datos:
  - `heart_rate`: Redondea a 2 decimales
  - `calories_burned`: Redondea a 2 decimales
  - `steps_daily`: Convierte a entero
  - `sleep_score`: Convierte de milisegundos a minutos si el valor es muy grande (>1,000,000)
  - Campos numéricos (`energy`, `stamina`, etc.): Redondea a 2 decimales

## Endpoint

```
POST /api/stats/snapshots/update-latest
```

## Headers Requeridos

```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

## Ejemplo 1: Datos básicos de salud (con nulls)

```bash
curl -X PATCH "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmEwMTI3NzctZmRhZi00ZWUxLWI0MWItYjU5ZjQ4Mzc0ZjU5IiwiZW1haWwiOiJkakB4eC5jb20iLCJuYW1lIjoiRGpva2VyIE0iLCJleHAiOjE3NjA3MTg1ODcsImlhdCI6MTc2MDYzMjE4N30.UonZrnr_sZjrdCO5CtTsoat0vCFDkP9cMud06GI5xEA" \
  -H "Content-Type: application/json" \
  -d '{
    "snapshot_at": "2025-10-16T16:33:36.947130Z",
    "energy": null,
    "stamina": null,
    "strength": null,
    "flexibility": null,
    "attention": null,
    "score_body": null,
    "score_mind": null,
    "model_version": "v1.0",
    "calories_burned": "0.0",
    "steps_daily": "94",
    "heart_rate": null,
    "sleep_score": "25200000",
    "inputs": null
  }'
```

**Respuesta esperada:**
- `snapshot_at`: "2025-10-16T16:33:36.947130Z"
- `model_version`: "v1.0"
- `calories_burned`: "3.76" (calculado: 94 pasos × 0.04 cal/paso)
- `steps_daily`: "94"
- `sleep_score`: "7.0 | bueno" (25,200,000 ms → 7 horas, óptimo)
- `heart_rate`: mantiene valor del snapshot anterior (si existe)
- Los campos con `null` NO se actualizarán y mantendrán sus valores anteriores

## Ejemplo 2: Actualización completa con todos los datos

```bash
curl -X PATCH "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmEwMTI3NzctZmRhZi00ZWUxLWI0MWItYjU5ZjQ4Mzc0ZjU5IiwiZW1haWwiOiJkakB4eC5jb20iLCJuYW1lIjoiRGpva2VyIE0iLCJleHAiOjE3NjA3MTg1ODcsImlhdCI6MTc2MDYzMjE4N30.UonZrnr_sZjrdCO5CtTsoat0vCFDkP9cMud06GI5xEA" \
  -H "Content-Type: application/json" \
  -d '{
    "snapshot_at": "2025-10-16T16:35:40.625Z",
    "energy": 85.5,
    "stamina": 72.3,
    "strength": 68.0,
    "flexibility": 55.0,
    "attention": 80.0,
    "score_body": 70.2,
    "score_mind": 80.0,
    "model_version": "v1.0",
    "calories_burned": "2500",
    "steps_daily": "10000",
    "heart_rate": "72",
    "sleep_score": "85",
    "inputs": {
      "task_count": 10,
      "workout_time": 60
    }
  }'
```

**Respuesta esperada:**
- Todos los campos se actualizarán con los nuevos valores
- Los números se redondearán a 2 decimales donde aplique

## Ejemplo 3: Actualización parcial (solo pasos y calorías)

```bash
curl -X PATCH "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "steps_daily": "15000",
    "calories_burned": "3200.5",
    "model_version": "v1.0"
  }'
```

## Ejemplo 4: Actualización con datos del móvil (Android Health Connect)

```bash
curl -X PATCH "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "snapshot_at": "2025-10-16T10:33:37.005Z",
    "model_version": "v1.0",
    "calories_burned": "125.75",
    "steps_daily": "5432",
    "heart_rate": "68.5",
    "sleep_score": "28800000"
  }'
```

**Procesamiento:**
- `calories_burned`: "125.75" → guardado como "125.75"
- `steps_daily`: "5432" → guardado como "5432"
- `heart_rate`: "68.5" → guardado como "68.5"
- `sleep_score`: "28800000" ms → "8.0 | bueno" (8 horas, dentro del rango óptimo)

## Ejemplo 5: Datos reales del móvil (DailySummary)

```bash
curl -X PATCH "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "snapshot_at": "2025-10-16T10:33:37.005Z",
    "energy": null,
    "stamina": null,
    "strength": null,
    "flexibility": null,
    "attention": null,
    "score_body": null,
    "score_mind": null,
    "model_version": "v1.0",
    "calories_burned": "0.0",
    "steps_daily": "94",
    "heart_rate": "67.25",
    "sleep_score": "25200000",
    "inputs": null
  }'
```

**Procesamiento automático:**
- `steps_daily`: "94" → guardado como "94"
- `calories_burned`: "0.0" → **calculado automáticamente**: "3.76" (94 × 0.04)
- `heart_rate`: "67.25" → guardado como "67.25"
- `sleep_score`: "25200000" ms → **convertido**: "7.0 | bueno"
  - Cálculo: 25,200,000 ms ÷ 1000 = 25,200 seg ÷ 60 = 420 min ÷ 60 = 7 horas
  - Clasificación: 7 horas = óptimo = "bueno"

## Formato de Respuesta Exitosa (200)

```json
{
  "id": "uuid-del-snapshot",
  "user_id": "6a012777-fdaf-4ee1-b41b-b59f48374f59",
  "snapshot_at": "2025-10-16T16:33:36.947130+00:00",
  "energy": 85.5,
  "stamina": 72.3,
  "strength": 68.0,
  "flexibility": 55.0,
  "attention": 80.0,
  "score_body": 70.2,
  "score_mind": 80.0,
  "model_version": "v1.0",
  "calories_burned": "125.75",
  "steps_daily": "5432",
  "heart_rate": "68.5",
  "sleep_score": "8.0 | bueno",
  "inputs": {
    "task_count": 10,
    "workout_time": 60
  }
}
```

## Errores Comunes

### 400 - No valid data to update
```json
{
  "error": "No valid data to update"
}
```
**Causa:** Todos los campos enviados son `null` o no hay campos válidos.

### 401 - Unauthorized
```json
{
  "error": "Unauthorized"
}
```
**Causa:** Token JWT inválido o expirado.

### 400 - Invalid request
```json
{
  "error": "Invalid request"
}
```
**Causa:** El cuerpo de la petición no es un JSON válido.

## Notas de Implementación

1. **Comportamiento con nulls:** Los campos con valor `null` son ignorados completamente. El snapshot mantiene sus valores anteriores para esos campos.

2. **Cálculo automático de calorías:** 
   - Si `calories_burned` llega como 0 o no se proporciona, se calcula automáticamente
   - Fórmula: `calorías = pasos × 0.04` (promedio para adulto)
   - Ejemplo: 94 pasos = 3.76 calorías

3. **Conversión y clasificación de sleep_score:**
   - **Conversión:** milisegundos → segundos → minutos → horas
   - **Clasificación:** 
     - 😊 **"bueno"**: 7-9 horas (óptimo)
     - 😐 **"estable"**: 6-7 o 9-10 horas (aceptable)
     - 😞 **"malo"**: <6 o >10 horas (insuficiente o excesivo)
   - **Formato guardado:** `"7.0 | bueno"`

4. **Manejo inteligente de heart_rate:**
   - Si llega un valor válido, se actualiza
   - Si llega `null` o no se proporciona, **mantiene el valor del snapshot anterior**
   - Esto evita perder datos cuando el sensor no reporta

5. **Creación automática:** Si el usuario no tiene ningún snapshot previo, el endpoint crea uno nuevo con los datos proporcionados.

6. **Timestamp automático:** Si no se proporciona `snapshot_at`, se usa la fecha/hora actual.

7. **Campos de texto:** `calories_burned`, `steps_daily`, `heart_rate`, y `sleep_score` se guardan como strings para mantener compatibilidad con diferentes fuentes de datos.

## Tabla de Clasificación de Sueño

| Horas de Sueño | Clasificación | Emoji | Descripción |
|----------------|---------------|-------|-------------|
| **7.0 - 9.0** | `bueno` | 😊 | Óptimo - Rango recomendado para adultos |
| **6.0 - 6.9** | `estable` | 😐 | Aceptable - Ligeramente por debajo |
| **9.1 - 10.0** | `estable` | 😐 | Aceptable - Ligeramente por encima |
| **< 6.0** | `malo` | 😞 | Insuficiente - Puede afectar rendimiento |
| **> 10.0** | `malo` | 😞 | Excesivo - Puede indicar problemas de salud |

### Ejemplos de conversión y clasificación:

```
25,200,000 ms → 7.0 horas → "bueno"
21,600,000 ms → 6.0 horas → "estable"
28,800,000 ms → 8.0 horas → "bueno"
32,400,000 ms → 9.0 horas → "bueno"
36,000,000 ms → 10.0 horas → "estable"
18,000,000 ms → 5.0 horas → "malo"
39,600,000 ms → 11.0 horas → "malo"
```

## Diferencias con POST /snapshots

| Característica | POST /snapshots | PATCH /snapshots/update-latest |
|----------------|-----------------|--------------------------------|
| Crea nuevo snapshot | ✅ Siempre | ❌ Solo si no existe uno |
| Actualiza snapshot existente | ❌ No | ✅ Sí (el más reciente) |
| Maneja nulls | ❌ Los guarda tal cual | ✅ Los ignora |
| Procesa/formatea datos | ❌ No | ✅ Sí |
| Calcula calorías de pasos | ❌ No | ✅ Sí (si calories = 0) |
| Convierte unidades | ❌ No | ✅ Sí (sleep_score ms → horas) |
| Clasifica calidad de sueño | ❌ No | ✅ Sí (malo/estable/bueno) |
| Mantiene heart_rate previo | ❌ No | ✅ Sí (si no llega nuevo) |
| Uso recomendado | Crear snapshots históricos | Actualizar datos en tiempo real desde móvil |
