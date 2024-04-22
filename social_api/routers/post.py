import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from social_api.database import database, comment_table, post_table
from social_api.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

from social_api.models.user import User
from social_api.security import get_current_user

logger = logging.getLogger(__name__)

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


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    logger.info("Getting all posts")
    query = post_table.select()

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
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
