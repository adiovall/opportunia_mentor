from fastapi import APIRouter, HTTPException
from backend.database import SessionLocal
from backend.models import User, Course
from passlib.context import CryptContext
from backend.schemas import UserCreate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from pydantic import BaseModel
from sqlalchemy import func
from emails import message


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



class EnrollRequest(BaseModel):
    username: str
    course_title: str



@router.post("/courses/enroll")
async def enroll_in_course(request: EnrollRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == request.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        course = db.query(Course).filter(Course.title == request.course_title).first()
        if not course:
            course = Course(title=request.course_title, description=f"Course: {request.course_title}")
            db.add(course)
        if course not in user.courses:
            user.courses.append(course)
            db.commit()
        return {"message": f"Enrolled in {request.course_title}", "courses": [{"id": c.id, "title": c.title, "description": c.description} for c in user.courses]}
    finally:
        db.close()


@router.post("/courses/enroll")
async def enroll_in_course(request: EnrollRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == request.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        course = db.query(Course).filter(func.lower(Course.title) == func.lower(request.course_title)).first()
        if not course:
            course = Course(title=request.course_title, description=f"Course: {request.course_title}")
            db.add(course)
        if course not in user.courses:
            user.courses.append(course)
            # Send email
            msg = MIMEMultipart()
            msg["From"] = "opportuniaoffice@gmail.com"
            msg["To"] = user.email
            msg["Subject"] = f"Enrollment in {request.course_title}"
            msg.attach(MIMEText(f"Dear {user.username}, you are enrolled in {request.course_title}. Start your journey!", "plain", "utf-8"))
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()
                    connection.login("opportuniaoffice@gmail.com", "rbtw cswq vejr dhzh")
                    connection.sendmail("opportuniaoffice@gmail.com", user.email, msg.as_string())
                    print(f"Email sent successfully to {user.email}")
            except smtplib.SMTPAuthenticationError as e:
                print(f"Authentication failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")
            except smtplib.SMTPException as e:
                print(f"SMTP error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"SMTP error: {str(e)}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
            db.commit()
        return {"message": f"Enrolled in {request.course_title}", "courses": [{"id": c.id, "title": c.title, "description": c.description} for c in user.courses]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        db.close()