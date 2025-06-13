from fastapi import APIRouter, HTTPException
from backend.database import SessionLocal
from backend.models import User
from passlib.context import CryptContext
from backend.schemas import UserCreate

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