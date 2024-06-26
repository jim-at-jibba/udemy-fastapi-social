import logging
from typing import Annotated
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy
from social_api.database import database, comment_table, post_table, like_table
from social_api.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
    PostLikeIn,
    PostLike,
    UserPostWithLikes,
)

from social_api.models.user import User
from social_api.security import get_current_user

logger = logging.getLogger(__name__)

select_post_and_likes = (
    sqlalchemy.select(post_table, sqlalchemy.func.count(like_table.c.id).label("likes"))
    .select_from(post_table.outerjoin(like_table))
    .group_by(post_table.c.id)
)

router = APIRouter()


async def find_post(post_id: int):
    logger.info("Find post")
    query = post_table.select().where(post_table.c.id == post_id)
    logging.debug(query)
    return await database.fetch_one(query)  # returns row not dict


# standard response code is 200, but creation should be 201
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(
    post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Creating post")
    data = {**post.model_dump(), "user_id": current_user.id}
    query = post_table.insert().values(data)
    logging.debug(query)
    last_record_id = await database.execute(query)
    # desctructures **
    return {**data, "id": last_record_id}


class PostSorting(str, Enum):
    new = "new"
    old = "old"
    likes = "likes"


@router.get("/post", response_model=list[UserPostWithLikes])
async def get_all_posts(
    sorting: PostSorting = PostSorting.new,
):  # because sorting is an enum not a pydanitc model, fastapi can infer it as a query param
    logger.info("Getting all posts")
    match sorting:
        case PostSorting.new:
            query = select_post_and_likes.order_by(post_table.c.id.desc())
        case PostSorting.old:
            query = select_post_and_likes.order_by(post_table.c.id.asc())
        case PostSorting.likes:
            query = select_post_and_likes.order_by(sqlalchemy.desc("likes"))
            # if sorting == PostSorting.new:
            #     query = select_post_and_likes.order_by(post_table.c.id.desc())
            # elif sorting == PostSorting.old:
            #     query = select_post_and_likes.order_by(post_table.c.id.asc())
            # elif sorting == PostSorting.likes:
            #     query = select_post_and_likes.order_by(sqlalchemy.desc("likes"))

            logging.debug(query)

    return await database.fetch_all(query)


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(
    comment: CommentIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Create comment")
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**comment.model_dump(), "user_id": current_user.id}
    query = comment_table.insert().values(data)
    logging.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    logger.info("Get comments on post")
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    logging.debug(query)
    return await database.fetch_all(query)  # returns sqlalcemy row


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    query = select_post_and_likes.where(post_table.c.id == post_id)

    logger.debug(query)
    post = await database.fetch_one(query)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }


@router.post("/like", response_model=PostLike, status_code=201)
async def like_post(
    like: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Liking post")

    post = await find_post(like.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {**like.dict(), "user_id": current_user.id}
    query = like_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
