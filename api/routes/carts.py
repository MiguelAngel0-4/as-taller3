from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from api.database import get_db
from api.models.cart import Cart, CartItem

router = APIRouter()

# Schemas
class CartItemAdd(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: Optional[str] = None
    product_price: Optional[float] = None

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOut] = []

    class Config:
        from_attributes = True

#Helpers
def _get_or_create_cart(user_id: int, db: Session) -> Cart:
    """Obtiene el carrito del usuario o lo crea si no existe."""
    carrito = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not carrito:
        carrito = Cart(user_id=user_id)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    return carrito


def _enrich_items(items: List[CartItem], db: Session) -> List[CartItemOut]:
    """Agrega nombre y precio del producto a cada item."""
    resultado = []
    for item in items:
        producto = db.query(Product).filter(Product.id == item.product_id).first()
        resultado.append(CartItemOut(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=producto.name if producto else None,
            product_price=float(producto.price) if producto else None,
        ))
    return resultado

@router.get("/{user_id}")
async def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar obtener carrito del usuario
    carrito = _get_or_create_cart(user_id, db)
    items = db.query(CartItem).filter(CartItem.cart_id == carrito.id).all()
    return {"id": carrito.id, "user_id": carrito.user_id, "items": _enrich_items(items, db)}

@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(data: CartItem, db: Session = Depends(get_db)):
    # TODO: Implementar agregar item al carrito
    producto = db.query(Product).filter(Product.id == data.product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock < data.quantity:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    carrito = _get_or_create_cart(data.user_id, db)

    item_existente = db.query(CartItem).filter(
        CartItem.cart_id == carrito.id,
        CartItem.product_id == data.product_id,
    ).first()

    if item_existente:
        item_existente.quantity += data.quantity
    else:
        nuevo_item = CartItem(cart_id=carrito.id, product_id=data.product_id, quantity=data.quantity)
        db.add(nuevo_item)

    db.commit()
    return {"message": "Producto agregado al carrito"}

@router.put("/items/{item_id}")
async def update_cart_item(item_id: int,data: CartItemUpdate, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar cantidad de item
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    item.quantity = data.quantity
    db.commit()
    return {"message": "Cantidad actualizada"}

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar remover item del carrito
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(item)
    db.commit()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(user_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar limpiar carrito
    carrito = db.query(Cart).filter(Cart.user_id == user_id).first()
    if carrito:
        db.query(CartItem).filter(CartItem.cart_id == carrito.id).delete()
        db.commit()