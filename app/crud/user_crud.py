from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from .base import CRUDBase
from app.models.user_model import User


class UserCRUD(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    pass


# Create a user instance
user_crud_obj = UserCRUD(User)
