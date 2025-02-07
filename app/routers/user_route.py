from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.schemas.user_schema import (
    UserCreateSchema,
    UserDetailsShowSchema,
    UserUpdateSchema,
)
from typing import List
from app.crud.user_crud import user_crud_obj

user_router = APIRouter()


@user_router.get("/users", response_model=List[UserDetailsShowSchema])
def get_user(db: Session = Depends(get_db)):
    users = user_crud_obj.get(db)
    return users


@user_router.get("/users/{id}", response_model=UserDetailsShowSchema)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = user_crud_obj.get_by_id(db, id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@user_router.post("/users", response_model=UserDetailsShowSchema)
def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        user = user_crud_obj.create(db, data)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.put("/users/{id}", response_model=UserDetailsShowSchema)
def update_user(id: int, data: UserUpdateSchema, db: Session = Depends(get_db)):
    db_obj = user_crud_obj.get_by_id(db, id)
    if db_obj:
        user_crud_obj.update(db, db_obj, data)
        return db_obj
    raise HTTPException(status_code=404, detail="User not found")


@user_router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = user_crud_obj.delete(db, id)
    return user
