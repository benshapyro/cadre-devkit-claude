# Flask API Examples

## Basic CRUD API

```python
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)

# Validation schemas
class UserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=0, max=150))

user_schema = UserSchema()

# List users
@app.route('/api/v1/users', methods=['GET'])
def list_users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 20))
    offset = (page - 1) * per_page

    users = db.user.find_many(skip=offset, take=per_page)
    total = db.user.count()
    total_pages = (total + per_page - 1) // per_page

    return jsonify({
        'data': users,
        'meta': {
            'total': total,
            'page': page,
            'perPage': per_page,
            'totalPages': total_pages,
        },
    })

# Get single user
@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.user.find_unique(where={'id': user_id})

    if not user:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'User not found',
            }
        }), 404

    return jsonify({'data': user})

# Create user
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.json)

        existing = db.user.find_unique(where={'email': data['email']})
        if existing:
            return jsonify({
                'error': {
                    'code': 'DUPLICATE',
                    'message': 'User with this email already exists',
                }
            }), 409

        user = db.user.create(data=data)
        return jsonify({'data': user}), 201

    except ValidationError as e:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid input data',
                'details': e.messages,
            }
        }), 400

# Update user
@app.route('/api/v1/users/<user_id>', methods=['PATCH'])
def update_user(user_id):
    try:
        data = user_schema.load(request.json, partial=True)

        user = db.user.update(
            where={'id': user_id},
            data=data,
        )
        return jsonify({'data': user})

    except ValidationError as e:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid input data',
                'details': e.messages,
            }
        }), 400

# Delete user
@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        db.user.delete(where={'id': user_id})
        return '', 204
    except Exception:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'User not found',
            }
        }), 404
```

## Authentication Decorator

```python
from functools import wraps
from flask import request, jsonify, g
import jwt
import os

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Authentication required',
                }
            }), 401

        try:
            payload = jwt.decode(
                token,
                os.getenv('JWT_SECRET'),
                algorithms=['HS256'],
            )
            g.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': {
                    'code': 'TOKEN_EXPIRED',
                    'message': 'Token has expired',
                }
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': 'Invalid token',
                }
            }), 401

        return f(*args, **kwargs)

    return decorated

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated(*args, **kwargs):
            if g.current_user.get('role') not in roles:
                return jsonify({
                    'error': {
                        'code': 'FORBIDDEN',
                        'message': 'Insufficient permissions',
                    }
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

# Usage
@app.route('/api/v1/users', methods=['GET'])
@require_auth
def list_users():
    pass

@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
@require_role('admin')
def delete_user(user_id):
    pass
```
