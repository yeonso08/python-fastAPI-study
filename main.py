from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas
import auth

# 서버 시작할 때 테이블이 없으면 자동으로 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.price = item.price
    db_item.is_available = item.is_available

    db.commit()
    db.refresh(db_item)
    return db_item

@app.patch("/items/{item_id}", response_model=schemas.ItemResponse)
def partial_update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # 클라이언트가 실제로 보낸 필드만 꺼내서, 그 필드만 반영 (나머지는 그대로 둠)
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

@app.get("/categories/")
def read_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@app.post("/categories/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.put("/categories/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.name = category.name

    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(email=user.email, hashed_password=auth.hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if user is None or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}