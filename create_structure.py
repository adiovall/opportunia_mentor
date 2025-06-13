import os
from pathlib import Path

# Define the project root
root = Path("opportunia_mentor")

# Define folder structure
folders = [
    root / ".venv",
    root / "backend" / "routes",
]

# Define files to create
files = [
    root / "backend" / "__init__.py",
    root / "backend" / "database.py",
    root / "backend" / "models.py",
    root / "backend" / "schemas.py",
    root / "backend" / "routes" / "__init__.py",
    root / "backend" / "routes" / "auth.py",
    root / "backend" / "routes" / "admin.py",
    root / "backend" / "routes" / "course.py",
    root / "backend" / "routes" / "user.py",
    root / "backend" / "routes" / "verify.py",
    root / "main.py",
    root / "init_db.py",
    root / ".env",
    root / "requirements.txt",
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file in files:
    file.touch(exist_ok=True)

print("✅ Project structure created successfully.")
