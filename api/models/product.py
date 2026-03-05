from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    # TODO: Definir los campos del modelo Product
    # id = Column(...)
    # name = Column(...)
    # description = Column(...)
    # price = Column(...)
    # stock = Column(...)
    # image_url = Column(...)
    # created_at = Column(...)
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    description = Column(Text)
    price       = Column(Numeric(10, 2), nullable=False, default=0.00)
    stock       = Column(Integer, nullable=False, default=0)
    image_url   = Column(Text)
    created_at  = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    def __repr__(self):
        # TODO: Implementar representación del objeto
        return f"<Product id={self.id} name={self.name!r} price={self.price}>"