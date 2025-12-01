# API Documentation Template

```markdown
# API Documentation

Base URL: `https://api.example.com/v1`

## Authentication

All API requests require a JWT token:

```
Authorization: Bearer <your_token>
```

## Rate Limiting

- 100 requests per 15 minutes per IP
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Pagination

```
GET /users?page=1&perPage=20
```

Response:
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20,
    "totalPages": 5
  },
  "links": {
    "first": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=2",
    "last": "/api/v1/users?page=5"
  }
}
```

## Error Responses

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [{ "field": "email", "message": "Invalid format" }]
  }
}
```

Common codes: VALIDATION_ERROR (400), UNAUTHORIZED (401), FORBIDDEN (403), NOT_FOUND (404)

## Endpoints

### List Resources

```
GET /api/v1/users
```

Query: `page`, `perPage`, `search`

### Get Resource

```
GET /api/v1/users/:id
```

### Create Resource

```
POST /api/v1/users
Content-Type: application/json

{ "name": "John", "email": "john@example.com" }
```

### Update Resource

```
PATCH /api/v1/users/:id
Content-Type: application/json

{ "name": "Jane" }
```

### Delete Resource

```
DELETE /api/v1/users/:id
```

## Code Examples

### JavaScript
```javascript
const response = await fetch('https://api.example.com/v1/users', {
  headers: { 'Authorization': 'Bearer TOKEN' }
});
const { data } = await response.json();
```

### Python
```python
import requests
response = requests.get(
    'https://api.example.com/v1/users',
    headers={'Authorization': 'Bearer TOKEN'}
)
data = response.json()['data']
```

### cURL
```bash
curl -X GET 'https://api.example.com/v1/users' \
  -H 'Authorization: Bearer TOKEN'
```
```
