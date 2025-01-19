import enum
from sqlalchemy import Column ,Integer ,String,Enum
from database.db import Base

class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)  