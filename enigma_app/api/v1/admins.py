from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from enigma_app.db import User
from enigma_app.db.session import get_db
from enigma_app.schemas.auth import TokenResponse
from enigma_app.services.auth_service import verify_password
from enigma_app.services.jwt_service import create_access_token

router = APIRouter(prefix="/admin", tags=["admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")


@router.post("/login", response_model=TokenResponse)
def admin_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username, User.role == "admin").first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь заблокирован")

    token = create_access_token({"sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": token, "token_type": "bearer"}
