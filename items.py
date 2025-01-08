from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.database import Item
from app.schemas import ItemCreate, ItemResponse
from starlette.responses import RedirectResponse

items_router = APIRouter(
    prefix="/items",
    tags=["Товары"],
)

@items_router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = Item(name=item.name, description=item.description, price=item.price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@items_router.get("/", response_model=list[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    if not items:
        raise HTTPException(status_code=404, detail="Товары не найдены")
    return items

@items_router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return item

@items_router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(item)
    db.commit()
    return item
