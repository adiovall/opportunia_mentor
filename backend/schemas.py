from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "securepass"
            }
        }