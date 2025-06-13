from fastapi import APIRouter, HTTPException
from backend.database import SessionLocal
from backend.models import User
from passlib.context import CryptContext
from backend.schemas import UserCreate
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.get("/test")
async def test():
    return {"message": "Auth test endpoint"}

@router.post("/register")
async def register(user: UserCreate):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = pwd_context.hash(user.password)
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        return {"message": "User registered successfully"}
    finally:
        db.close()

@router.post("/login")
async def login(login_data: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == login_data.username).first()
        if not user or not pwd_context.verify(login_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful"}
    finally:
        db.close()

@router.get("/me")
async def get_current_user(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": user.username, "bio": user.profile.bio if user.profile else None}
    finally:
        db.close()

@router.get("/courses")
async def get_user_courses(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        courses = [{"id": c.id, "title": c.title, "description": c.description} for c in user.courses]
        return {"username": user.username, "courses": courses}
    finally:
        db.close()