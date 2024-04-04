from pydantic import BaseModel, ConfigDict
# BaseModel allows us to validate our request


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    # this tells pydantic to treat model as row or dict
    model_config = ConfigDict(from_attributes=True)

    id: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    # this tells pydantic to treat model as row or dict
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
