import logging

from fastapi import APIRouter, HTTPException, status
from social_api.models.user import UserIn
from social_api.database import database, user_table
from social_api.security import (
    get_user,
    get_password_hash,
    authenticate_user,
    create_access_token,
)


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)
    logger.debug(query)
    user_id = await database.execute(query)
    return {"id": user_id, "email": user.email}


@router.post("/token")
async def login(user: UserIn):
    await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
