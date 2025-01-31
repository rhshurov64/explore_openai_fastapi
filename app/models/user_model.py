from sqlalchemy import (
    String,
    Integer,
    Column,
    Boolean,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database.session import Base

# Association for m2m field
user_group_association = Table(
    "user_group_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column(
        "group_id",
        ForeignKey("groups.id"),
        primary_key=True,
    ),
    # UniqueConstraint("user_id", "group_id", name="user_group_id_unique_pair"),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    # Define the one-to-one relationship, uselist will restrict to submit multiple profiles.
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    images = relationship("UserImage", back_populates="user")

    groups = relationship(
        "Group", secondary=user_group_association, back_populates="users"
    )


# One to one relationship with user model
class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String, nullable=True)

    # Store the user id for profile, unique=True force so that on user id can assign to only one profile
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="profile")


# One to Many relationship with user model
class UserImage(Base):
    __tablename__ = "user_images"
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="images")


# Many to Many relationship with user model
class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    users = relationship(
        "User", secondary=user_group_association, back_populates="groups"
    )
