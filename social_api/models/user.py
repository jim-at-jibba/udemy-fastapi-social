from pydantic import BaseModel


# model for user, password is not included in the response
class User(BaseModel):
    id: int | None = None
    email: str


# model for user creation
class UserIn(User):
    password: str
