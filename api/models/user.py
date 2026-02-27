from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from api.database import Base

class User(Base):
    __tablename__ = "users"
    
    # TODO: Definir los campos del modelo User
    # id = Column(...)
    # username = Column(...)
    # email = Column(...)
    # password_hash = Column(...)
    # is_active = Column(...)
    # created_at = Column(...)
    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50),  unique=True, nullable=False)
    email         = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active     = Column(Boolean, nullable=False, default=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        # TODO: Implementar representación del objeto
        return f"<User id={self.id} username={self.username!r}>"
