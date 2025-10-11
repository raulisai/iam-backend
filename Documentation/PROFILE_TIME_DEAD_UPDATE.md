# Profile - Campos time_dead y day_work

## Resumen

Se han agregado dos campos nuevos a la tabla de perfiles:
- `time_dead`: Para rastrear el tiempo muerto o no productivo del usuario
- `day_work`: Para especificar los días de trabajo en la semana

## Campos Agregados

### time_dead
- **Tipo**: `numeric` (number)
- **Valor por defecto**: `0`
- **Descripción**: Tiempo muerto o no productivo rastreado para el usuario
- **Ejemplo**: `5.0`

### day_work
- **Tipo**: `text` (string)
- **Valor por defecto**: `NULL`
- **Descripción**: Días de trabajo en la semana en formato D,L,M,M,J,V,S
- **Formato**: D=Domingo, L=Lunes, M=Martes, M=Miércoles, J=Jueves, V=Viernes, S=Sábado
- **Ejemplo**: `"L,M,M,J,V"` (Lunes a Viernes)

## Cambios Realizados

### 1. Base de Datos (profiles_schema.sql)
```sql
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS time_dead NUMERIC DEFAULT 0;

ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS day_work TEXT DEFAULT NULL;
```

### 2. API Routes (routes/profile_routes.py)
Se agregaron `time_dead` y `day_work` a toda la documentación Swagger en los siguientes endpoints:

- **GET /api/profile/** - Respuesta incluye time_dead y day_work
- **POST /api/profile/** - Request y respuesta incluyen time_dead y day_work
- **PUT /api/profile/** - Request y respuesta incluyen time_dead y day_work

### 3. Swagger Documentation
Los campos aparecen en todos los schemas con las siguientes características:

**time_dead - En Request (POST/PUT)**:
```yaml
time_dead:
  type: number
  example: 0
  description: Tiempo muerto o no productivo
```

**time_dead - En Response**:
```yaml
time_dead:
  type: number
  example: 0
```

**day_work - En Request (POST/PUT)**:
```yaml
day_work:
  type: string
  example: "L,M,M,J,V"
  description: Días de trabajo en la semana (D,L,M,M,J,V,S)
```

**day_work - En Response**:
```yaml
day_work:
  type: string
  example: "L,M,M,J,V"
```

## Migración de Base de Datos

Para aplicar los cambios en la base de datos, ejecutar:

```bash
psql -U your_user -d your_database -f profiles_schema.sql
```

O ejecutar directamente:

```sql
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS time_dead NUMERIC DEFAULT 0;

ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS day_work TEXT DEFAULT NULL;
```

## Uso en API

### Crear Perfil con time_dead y day_work

```bash
curl -X POST https://your-api.com/api/profile/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "timezone": "America/Mexico_City",
    "birth_date": "1990-01-15",
    "gender": "male",
    "weight_kg": 75.5,
    "height_cm": 175,
    "preferred_language": "es",
    "hours_available_to_week": 40,
    "work_schedules": "9:00-17:00",
    "current_status": "active",
    "hours_used_to_week": 0,
    "time_dead": 0,
    "day_work": "L,M,M,J,V"
  }'
```

### Actualizar time_dead y day_work

```bash
curl -X PUT https://your-api.com/api/profile/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "time_dead": 5.0,
    "day_work": "L,M,M,J,V,S"
  }'
```

### Obtener Perfil (incluye time_dead)

```bash
curl -X GET https://your-api.com/api/profile/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Respuesta de ejemplo**:
```json
{
  "id": "uuid-here",
  "user_id": "user-uuid-here",
  "timezone": "America/Mexico_City",
  "birth_date": "1990-01-15",
  "gender": "male",
  "weight_kg": 75.5,
  "height_cm": 175,
  "preferred_language": "es",
  "hours_available_to_week": 40,
  "work_schedules": "9:00-17:00",
  "current_status": "active",
  "hours_used_to_week": 25.5,
  "time_dead": 5.0,
  "day_work": "L,M,M,J,V",
  "created_at": "2025-01-15T10:30:00Z"
}
```

## Notas Importantes

### time_dead
1. El campo es **opcional** en las peticiones POST y PUT
2. El valor por defecto es `0` si no se especifica
3. Los valores deben ser numéricos (pueden incluir decimales)
4. El campo se incluye automáticamente en todas las respuestas de perfil

### day_work
1. El campo es **opcional** en las peticiones POST y PUT
2. El valor por defecto es `NULL` si no se especifica
3. **Formato**: String con días separados por comas (D,L,M,M,J,V,S)
   - D = Domingo
   - L = Lunes
   - M = Martes (primero)
   - M = Miércoles (segundo)
   - J = Jueves
   - V = Viernes
   - S = Sábado
4. **Ejemplos válidos**:
   - `"L,M,M,J,V"` (Lunes a Viernes)
   - `"L,M,J,V"` (Lunes, Martes, Jueves, Viernes)
   - `"S,D"` (Sábado y Domingo)
   - `"L,M,M,J,V,S,D"` (Toda la semana)
5. El campo se incluye automáticamente en todas las respuestas de perfil

### General
**No se requieren cambios en el código del servicio o controlador** - Supabase maneja automáticamente los nuevos campos

## Compatibilidad

- ✅ Los cambios son **retrocompatibles**
  - Perfiles existentes tendrán `time_dead = 0` por defecto
  - Perfiles existentes tendrán `day_work = NULL` por defecto
- ✅ Los clientes que no envíen los campos seguirán funcionando correctamente
- ✅ Los clientes que consulten perfiles recibirán los campos automáticamente

## Archivos Modificados

1. `profiles_schema.sql` (nuevo) - Script de migración con ambos campos
2. `routes/profile_routes.py` - Documentación Swagger actualizada con time_dead y day_work
3. `Documentation/API_Auth_Profile.md` - Ejemplos actualizados
4. `Documentation/PROFILE_TIME_DEAD_UPDATE.md` (este archivo) - Documentación de los cambios
