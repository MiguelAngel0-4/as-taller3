from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from api.database import get_db
from api.models.user import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Shemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(data: UserRegister, db: Session = Depends(get_db)):
    # TODO: Implementar registro de usuario
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    nuevo_usuario = User(
        username=data.username,
        email=data.email,
        password_hash=pwd_context.hash(data.password),
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login")  
async def login_user(data: UserLogin, db: Session = Depends(get_db)):
    # TODO: Implementar login de usuario
    usuario = db.query(User).filter(User.username == data.username).first()
    if not usuario or not pwd_context.verify(data.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not usuario.is_active:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")

    return {"id": usuario.id, "username": usuario.username, "email": usuario.email}

@router.get("/profile/{user_id}", response_model=UserOut)
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar obtener perfil de usuario
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/profile/{user_id}", response_model=UserOut)
async def update_user_profile(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar perfil de usuario
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if data.email:
        usuario.email = data.email
    if data.password:
        usuario.password_hash = pwd_context.hash(data.password)

    db.commit()
    db.refresh(usuario)
    return usuario