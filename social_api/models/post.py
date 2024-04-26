from pydantic import BaseModel, ConfigDict
# BaseModel allows us to validate our request


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    # this tells pydantic to treat model as row or dict, replaces orm_mode=True
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserPostWithLikes(UserPost):
    model_config = ConfigDict(from_attributes=True)

    likes: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    # this tells pydantic to treat model as row or dict
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserPostWithComments(BaseModel):
    post: UserPostWithLikes
    comments: list[Comment]


class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    id: int
    user_id: int
