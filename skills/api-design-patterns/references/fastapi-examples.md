# FastAPI API Examples

## Basic CRUD API

```python
from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

app = FastAPI()

# Request/Response models
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    age: Optional[int]

class PaginatedResponse(BaseModel):
    data: List[UserResponse]
    meta: dict
    links: dict

# List users with pagination
@app.get("/api/v1/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    offset = (page - 1) * per_page

    users = await db.user.find_many(skip=offset, take=per_page)
    total = await db.user.count()
    total_pages = (total + per_page - 1) // per_page

    return {
        "data": users,
        "meta": {
            "total": total,
            "page": page,
            "perPage": per_page,
            "totalPages": total_pages,
        },
        "links": {
            "first": f"/api/v1/users?page=1&per_page={per_page}",
            "prev": f"/api/v1/users?page={page-1}&per_page={per_page}" if page > 1 else None,
            "next": f"/api/v1/users?page={page+1}&per_page={per_page}" if page < total_pages else None,
            "last": f"/api/v1/users?page={total_pages}&per_page={per_page}",
        },
    }

# Get single user
@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await db.user.find_unique(where={"id": user_id})

    if not user:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "User not found"},
        )

    return user

# Create user
@app.post("/api/v1/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    existing = await db.user.find_unique(where={"email": user.email})

    if existing:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "DUPLICATE",
                "message": "User with this email already exists",
            },
        )

    new_user = await db.user.create(data=user.model_dump())
    return new_user

# Update user
@app.patch("/api/v1/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdate):
    update_data = user.model_dump(exclude_unset=True)

    try:
        updated_user = await db.user.update(
            where={"id": user_id},
            data=update_data,
        )
        return updated_user
    except Exception:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "User not found"},
        )

# Delete user
@app.delete("/api/v1/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    try:
        await db.user.delete(where={"id": user_id})
    except Exception:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "User not found"},
        )
```

## Authentication & Authorization

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"],
        )
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "INVALID_TOKEN", "message": "Invalid token"},
            )

        user = await db.user.find_unique(where={"id": user_id})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "USER_NOT_FOUND", "message": "User not found"},
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"},
        )

def require_role(*roles: str):
    async def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": "Insufficient permissions"},
            )
        return user

    return role_checker

# Usage
@app.get("/api/v1/users", dependencies=[Depends(get_current_user)])
async def list_users():
    pass

@app.delete("/api/v1/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_role("admin")),
):
    pass
```
