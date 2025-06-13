from backend.database import SessionLocal
from backend.models import User

session = SessionLocal()
users = session.query(User).all()
for u in users:
    print(f'{u.username}: {u.profile.bio if u.profile else "No profile"}')
session.close()