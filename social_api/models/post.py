from pydantic import BaseModel
# BaseModel allows us to validate our request


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int
