from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import user_model
from app.schemas.user_schema import (
    UserCreateSchema,
    UserDetailsShowSchema,
    UserUpdateSchema,
    CreateUserProfileSchema,
)
from fastapi.encoders import jsonable_encoder
import json
from typing import List

from app.crud.user_crud import user_crud_obj

user_router = APIRouter()


# @user_router.get("/users")
# def get_users(db: Session = Depends(get_db)):
#     users = db.query(user_model.User).all()
#     # print(users.count())

#     return users


# @user_router.post("/users/app")
# def create_user_(data: UserCreateSchema, db: Session = Depends(get_db)):
#     data = data.model_dump()

#     print(data)
#     print(type(data))
#     # x = user_model.User(username=data.username, password=data.password, name=data.name)
#     try:
#         user_data = user_model.User(**data)
#         db.add(user_data)
#         db.commit()
#         return user_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


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


@user_router.post("/users-profile")
def create_user_profile(data: CreateUserProfileSchema, db: Session = Depends(get_db)):
    user = user_crud_obj.get_by_id(db, data.user_id)
    # print(user.profile.user.name)

    if user:
        # user_profile = user_model.UserProfile(user_id=user.id, bio=data.bio)

        # It will create a new profile, if its already exists delete the user_id from that one create a new everytime.
        # SQLAlchemy automatically updates the existing profile's user_id to NULL and assigns the user to the new profile.
        # new_profile = user_model.UserProfile(bio=data.bio, user=user)
        # print(new_profile)

        # Create and link the profile directly
        # It will create a new profile, if its already exists delete the user_id from that one create a new everytime.
        # SQLAlchemy automatically updates the existing profile's user_id to NULL and assigns the user to the new profile.
        # user.profile = user_model.UserProfile(bio=data.bio)

        # db.add(user_profile)
        # db.commit()
        #     return user_profile

        # Access Data, with back_populates: profile and user
        # print(user.profile)
        # print(user.profile.bio)
        # print(user.profile.user)
        # print(user.profile.user.name)

        # profile = (
        #     db.query(user_model.UserProfile)
        #     .filter(user_model.UserProfile.user_id == user.id)
        #     .first()
        # )
        # print(profile.bio)

        # join query for fetch related data also, like prefetch and select_related
        # profile = (
        #     db.query(user_model.UserProfile)
        #     .join(user_model.User)
        #     .filter(user_model.User.id == user.id)
        #     .first()
        # )
        # print(profile.bio)

        # profile = (
        #     db.query(user_model.UserProfile)
        #     .join(user_model.User)
        #     .filter(user_model.UserProfile.id == user.profile.id)
        #     .first()
        # )
        # print(profile.bio)

        # user_image = user_model.UserImage(image_name="one", user=user)

        # image1 = user_model.UserImage(image_name="append 1", user_id=user.id)
        # image2 = user_model.UserImage(image_name="append 2", user_id=user.id)
        # user.images.append(image1)
        # user.images.append(image2)

        # db.add(user_image)
        # db.commit()

        # images = (
        #     db.query(user_model.UserImage)
        #     .filter(user_model.UserImage.user_id == user.id)
        #     .all()
        # )
        # print(images[-1].image_name)

        # image_user = (
        #     db.query(user_model.User)
        #     .join(user_model.UserImage)
        #     .filter(user_model.UserImage.id == 8)
        #     .all()
        # )

        # print(image_user[0].name)

        # single object assign
        group = db.query(user_model.Group).get(2)
        print(group)

        # This will assign same thing again and again
        # user.groups.append(group)

        ## Assign only if not already assigned
        # if group not in user.groups:
        #     user.groups.append(group)
        # db.commit()

        ## multiple objects assign
        # groups = db.query(user_model.Group).filter(user_model.Group.id.in_([1, 2])).all()
        # user.groups.extend(groups)

        ## Remove single object
        # Raise error if same group assigned for same user multiple times
        # Prevent same pair assigned multiple times by cheeck: if group not in user.groups:
        # Raise error if association not found: ValueError: list.remove(x): x not in list
        # user.groups.remove(group)

        ## errro: 'user_group_association' expected to delete 1 row(s); Only 2 were matched.

        ## use so that not raise error if not found.
        # if group in user.groups:
        #     user.groups.remove(group)

        ## Solution, it will removed all
        ## It will not raise any error, if association not found
        # db.query(user_model.user_group_association).filter(
        #     user_model.user_group_association.c.user_id == user.id,
        #     user_model.user_group_association.c.group_id == group.id,
        # ).delete(synchronize_session=False)

        # Clear all from the m2m field
        # user.groups.clear()

        print("Assigned")

        # db.commit()

        # Access Data

        ## Get all groups for user
        # groups = user.groups

        ## Get all users for group
        # users = group.users

        # users = db.query(user_model.User).filter(user_model.User.name == "string")
        # user = users.filter(user_model.User.id.in_([3, 8])).all()
        # print(user)

        # groups = db.query(user_model.Group).all()
        # user.groups.remove(groups)

        # fetch groups of a user with join
        groups = (
            db.query(user_model.Group)
            .join(user_model.User)
            .filter(user_model.User.id == 3)
            .all()
        )

        print(groups)

    return
