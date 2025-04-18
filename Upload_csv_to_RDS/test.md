### 📁 Full Folder Structure: returns-management/backend/app

returns-management/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── docker-compose.yml
├── README.md

### ==============================
### 1️⃣ File: core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

settings = Settings()

### ==============================
### 2️⃣ File: db/session.py

import mysql.connector
from app.core.config import settings

def get_db():
    return mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )

### ==============================
### 3️⃣ File: models/user.py

# Not needed if using MySQL directly, but can use SQLAlchemy if needed

### ==============================
### 4️⃣ File: schemas/user.py

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str

### ==============================
### 5️⃣ File: api/v1/auth.py

from fastapi import APIRouter, HTTPException, Form
from app.schemas.user import UserCreate, UserLogin, ForgotPassword, ResetPassword
from app.db.session import get_db
from app.core.config import settings
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import smtplib

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register(user: UserCreate):
    db = get_db()
    cursor = db.cursor()
    try:
        hashed_password = pwd_context.hash(user.password)
        cursor.execute("INSERT INTO users (email, hashed_password, full_name) VALUES (%s, %s, %s)",
                       (user.email, hashed_password, user.full_name))
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        cursor.close()
        db.close()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE email = %s", (user.email,))
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if result and pwd_context.verify(user.password, result[0]):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/forgot-password")
def forgot_password(data: ForgotPassword):
    token = jwt.encode({"sub": data.email, "exp": datetime.utcnow() + timedelta(minutes=30)},
                       settings.SECRET_KEY, algorithm="HS256")
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            subject = "Password Reset"
            body = f"Click the link to reset your password: {reset_link}"
            msg = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(settings.EMAIL_USER, data.email, msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

    return {"message": "Reset link sent"}

@router.post("/reset-password")
def reset_password(reset: ResetPassword):
    try:
        payload = jwt.decode(reset.token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    hashed_password = pwd_context.hash(reset.new_password)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET hashed_password = %s WHERE email = %s", (hashed_password, email))
    db.commit()
    cursor.close()
    db.close()

    return {"message": "Password reset successful"}

### ==============================
### 6️⃣ File: main.py

from fastapi import FastAPI
from app.api.v1 import auth

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth")

@app.get("/")
def root():
    return {"message": "Welcome to Returns Management Auth API"}

### ==============================
### 7️⃣ File: .env (store in backend/ folder)

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=returns_db
SECRET_KEY=asecretkeyhere
EMAIL_USER=yourgmail@gmail.com
EMAIL_PASS=your_app_password

### ==============================
### ✅ Done!
- Register → `/api/v1/auth/register`
- Login → `/api/v1/auth/login`
- Forgot Password → `/api/v1/auth/forgot-password`
- Reset Password → `/api/v1/auth/reset-password`
 unit tests or frontend integration with Vue.js ✨
