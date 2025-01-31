from typing import Any, Type, Generic, List, Optional, TypeVar, Union, Dict
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database.session import Base
from fastapi import HTTPException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the CRUD operations for a given SQLAlchemy model.

        params:
        model (Type[ModelType]): Refers to any SQLAlchemy model class.

        """
        self.model = model

    def get(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, data: CreateSchemaType) -> ModelType:
        dict_data = jsonable_encoder(data)
        db_obj = self.model(**dict_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        data: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        dict_obj_data = jsonable_encoder(db_obj)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)

        for field in dict_obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Any) -> ModelType:
        db_obj = db.query(self.model).get(id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return db_obj
        raise HTTPException(status_code=404, detail="User Not Found")
