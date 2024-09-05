from sqlalchemy import Column, Integer, String, Boolean
from app.database.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    token = relationship("Token", back_populates="user",
                         cascade="all, delete-orphan")  # Link user with a token
