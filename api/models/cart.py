from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base

class Cart(Base):
    __tablename__ = "carts"
    
    # TODO: Definir los campos del modelo Cart
    # id = Column(...)
    # user_id = Column(..., ForeignKey(...))
    # created_at = Column(...)
    # updated_at = Column(...)
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    # TODO: Definir relaciones
    # user = relationship(...)
    # items = relationship(...)
    user  = relationship("User",     back_populates=None)
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart id={self.id} user_id={self.user_id}>"

class CartItem(Base):
    __tablename__ = "cart_items"
    
    # TODO: Definir los campos del modelo CartItem
    # id = Column(...)
    # cart_id = Column(..., ForeignKey(...))
    # product_id = Column(..., ForeignKey(...))
    # quantity = Column(...)
    # added_at = Column(...)
    id         = Column(Integer, primary_key=True, index=True)
    cart_id    = Column(Integer, ForeignKey("carts.id",    ondelete="CASCADE"),  nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    quantity   = Column(Integer, nullable=False, default=1)
    added_at   = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    # TODO: Definir relaciones
    # cart = relationship(...)
    # product = relationship(...)
    cart    = relationship("Cart",    back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<CartItem id={self.id} cart_id={self.cart_id} product_id={self.product_id} qty={self.quantity}>"