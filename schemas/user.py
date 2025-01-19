from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    hashed_password: str
    role: str = "user"