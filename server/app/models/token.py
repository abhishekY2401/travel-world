from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="token")


class RefreshToken(Base):
    __tablename__ = "refresh"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    device_id = Column(String, index=True)
