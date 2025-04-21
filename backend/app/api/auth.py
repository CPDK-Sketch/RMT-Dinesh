from fastapi import APIRouter, HTTPException
from app.schemas.user import UserLogin, TokenResponse
from app.services.auth import create_jwt_token, users_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    db_user = users_db.get(user.username)
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token({"sub": user.username, "role": db_user["role"]})
    return {"access_token": token, "role": db_user["role"]}