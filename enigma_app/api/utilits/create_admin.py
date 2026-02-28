from sqlalchemy.orm import Session

from enigma_app.db.models.user import User
from enigma_app.db.session import get_db
from enigma_app.services.auth_service import hash_password

def create_default_admin():
    db: Session = next(get_db())

    admin_email = "admin@example.com"
    admin_password = "supersecurepassword"
    role = "admin"

    existing = db.query(User).filter(User.email == admin_email).first()
    if existing:
        print("Админ уже существует")
        return existing

    admin = User(
        email=admin_email,
        password_hash=hash_password(admin_password),
        role=role
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"Создан админ: {admin_email} / {admin_password}")
    return admin