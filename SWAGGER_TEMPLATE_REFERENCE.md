# Documentación Swagger - Plantilla de Referencia

Este archivo contiene las plantillas de documentación Swagger para cada tipo de endpoint.

## Estructura Base de Swagger Doc

```python
"""Endpoint description.
---
tags:
  - Tag Name
parameters:
  - in: header
    name: Authorization
    description: JWT token (Bearer <token>)
    required: true
    type: string
  - in: path/query/body
    name: parameter_name
    description: Parameter description
    required: true/false
    type: string/integer/object
    schema:  # For body parameters
      type: object
      properties:
        field_name:
          type: string
          example: "example value"
          description: "Field description"
responses:
  200:
    description: Success description
    schema:
      type: object/array
      properties:  # or items: for arrays
        field_name:
          type: string
          example: "example"
  400:
    description: Bad Request
    schema:
      $ref: '#/definitions/ErrorResponse'
  401:
    description: Unauthorized
    schema:
      $ref: '#/definitions/ErrorResponse'
"""
```

## Plantilla para GET (List)

```python
@route.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_items():
    """Get all items for authenticated user.
    ---
    tags:
      - Items
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: filter_param
        type: string
        required: false
        description: Optional filter
        example: "value"
    responses:
      200:
        description: List of items
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                format: uuid
              name:
                type: string
                example: "Item name"
              created_at:
                type: string
                format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_all_items()
```

## Plantilla para GET (Single Item)

```python
@route.route('/<item_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_item(item_id):
    """Get item by ID.
    ---
    tags:
      - Items
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: item_id
        in: path
        required: true
        type: string
        format: uuid
        description: Item ID
    responses:
      200:
        description: Item data
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            created_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Item belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Item not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_item_by_id(item_id)
```

## Plantilla para POST (Create)

```python
@route.route('/', methods=['POST', 'OPTIONS'])
@token_required
def create_item():
    """Create new item.
    ---
    tags:
      - Items
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Item data
        required: true
        schema:
          type: object
          required:
            - name
            - description
          properties:
            name:
              type: string
              example: "Item name"
              description: Name of the item
            description:
              type: string
              example: "Item description"
              description: Description text
            optional_field:
              type: string
              example: "optional"
              description: Optional field
    responses:
      201:
        description: Item created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            description:
              type: string
            created_at:
              type: string
              format: date-time
      400:
        description: Invalid request or missing required fields
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_new_item(data)
```

## Plantilla para PUT (Update)

```python
@route.route('/<item_id>', methods=['PUT', 'OPTIONS'])
@token_required
def update_item(item_id):
    """Update item.
    ---
    tags:
      - Items
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: item_id
        in: path
        required: true
        type: string
        format: uuid
        description: Item ID
      - in: body
        name: body
        description: Updated item data (only include fields to update)
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Updated name"
            description:
              type: string
              example: "Updated description"
    responses:
      200:
        description: Item updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            description:
              type: string
            updated_at:
              type: string
              format: date-time
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Item belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Item not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_item_data(item_id, data)
```

## Plantilla para DELETE

```python
@route.route('/<item_id>', methods=['DELETE', 'OPTIONS'])
@token_required
def delete_item(item_id):
    """Delete item.
    ---
    tags:
      - Items
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: item_id
        in: path
        required: true
        type: string
        format: uuid
        description: Item ID to delete
    responses:
      200:
        description: Item deleted successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Item belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Item not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return delete_item_by_id(item_id)
```

## Tipos de Datos Comunes

### UUID
```yaml
type: string
format: uuid
```

### Date-Time
```yaml
type: string
format: date-time
example: "2025-10-01T10:00:00Z"
```

### Date
```yaml
type: string
format: date
example: "2025-10-01"
```

### Enum
```yaml
type: string
enum: ["option1", "option2", "option3"]
example: "option1"
```

### JSONB Object
```yaml
type: object
example: {"key": "value", "nested": {"data": 123}}
description: "Flexible JSON data"
```

### Array
```yaml
type: array
items:
  type: string
example: ["item1", "item2", "item3"]
```

## Respuestas de Error Estándar

Todas las respuestas de error deben usar:
```yaml
401:
  description: Unauthorized - Invalid or missing token
  schema:
    $ref: '#/definitions/ErrorResponse'
403:
  description: Forbidden - Access denied
  schema:
    $ref: '#/definitions/ErrorResponse'
404:
  description: Not found
  schema:
    $ref: '#/definitions/ErrorResponse'
400:
  description: Bad request
  schema:
    $ref: '#/definitions/ErrorResponse'
500:
  description: Internal server error
  schema:
    $ref: '#/definitions/ErrorResponse'
```

## Tags por Módulo

- **Auth** - Autenticación
- **Profile** - Perfiles de usuario
- **Task Templates** - Plantillas de tareas
- **Mind Tasks** - Tareas de mente
- **Body Tasks** - Tareas de cuerpo
- **Achievements** - Logros
- **Goals** - Metas
- **Task Logs** - Registros de tareas
- **Failures** - Fallos
- **Bot Rules** - Reglas del bot
- **Chat IA** - Chat con IA

## Notas Importantes

1. **Siempre incluir Authorization header** en endpoints protegidos
2. **Usar format: uuid** para IDs que son UUID
3. **Incluir ejemplos** en todos los campos cuando sea posible
4. **Documentar query parameters** con `in: query`
5. **Usar enums** para valores predefinidos
6. **Incluir descripciones claras** en español o inglés consistente
7. **Respuestas de error** deben ser consistentes
8. **OPTIONS method** debe devolver 200 vacío para CORS
