# Quick Reference: day_work Field

## Campo day_work

**Tipo**: TEXT (string)  
**Descripción**: Días de trabajo en la semana  
**Formato**: D,L,M,M,J,V,S  
**Default**: NULL  

## Formato de Días

| Letra | Día |
|-------|-----|
| D | Domingo |
| L | Lunes |
| M | Martes |
| M | Miércoles ⚠️ |
| J | Jueves |
| V | Viernes |
| S | Sábado |

⚠️ **Importante**: Hay dos "M" en la secuencia completa

## Ejemplos

```json
"day_work": "L,M,M,J,V"      // Lunes a Viernes
"day_work": "L,M,J,V"        // Lunes, Martes, Jueves, Viernes
"day_work": "S,D"            // Fin de semana
"day_work": "D,L,M,M,J,V,S"  // Toda la semana
"day_work": null             // No especificado
```

## Migración SQL

```sql
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS day_work TEXT DEFAULT NULL;
```

## API Endpoints

✅ **GET** `/api/profile/` - Devuelve day_work  
✅ **POST** `/api/profile/` - Acepta day_work (opcional)  
✅ **PUT** `/api/profile/` - Actualiza day_work (opcional)  

## Ejemplo cURL

```bash
# Crear con day_work
curl -X POST https://api.com/api/profile/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"timezone": "America/Mexico_City", "day_work": "L,M,M,J,V"}'

# Actualizar day_work
curl -X PUT https://api.com/api/profile/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"day_work": "L,M,M,J,V,S"}'
```

---

📖 **Documentación completa**: `PROFILE_DAY_WORK_FINAL_SUMMARY.md`
