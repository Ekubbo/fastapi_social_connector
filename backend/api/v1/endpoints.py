from typing import List, Optional

from fastapi import APIRouter, HTTPException
from social import base as social_api
from social.exceptions import SocialException, UserDoesNotExist

from .schemas import Article, Source, User

api_router = APIRouter()


@api_router.get(
    "/user/{user_id}", response_model=User, responses={404: {}, 500: {}}
)
def get_user(user_id: str, source: Optional[Source] = None):

    try:
        user = social_api.get_user(user_id, source)
    except UserDoesNotExist:
        raise HTTPException(status_code=404)
    except SocialException:
        raise HTTPException(status_code=500)

    return user.dict()


@api_router.get(
    "/user/{user_id}/article", response_model=List[Article],
    responses={404: {}, 500: {}}
)
def get_articles(
    user_id: str, source: Optional[Source] = None, count: int = 10
):

    try:
        articles = social_api.get_articles(user_id, count, source)
    except UserDoesNotExist:
        raise HTTPException(status_code=404)
    except SocialException:
        raise HTTPException(status_code=500)

    return list(map(lambda x: x.dict(), articles))


@api_router.get(
    "/user/{user_id}/friend", response_model=List[User],
    responses={404: {}, 500: {}}
)
def get_friends(
    user_id: str, source: Optional[Source] = None, count: int = 10
):

    try:
        users = social_api.get_friends(user_id, count, source)
    except UserDoesNotExist:
        raise HTTPException(status_code=404)
    except SocialException:
        raise HTTPException(status_code=500)

    return list(map(lambda x: x.dict(), users))


@api_router.get(
    "/user/{user_id}/follower", response_model=List[User],
    responses={404: {}, 500: {}}
)
def get_followers(
    user_id: str, source: Optional[Source] = None, count: int = 10
):

    try:
        users = social_api.get_followers(user_id, count, source)
    except UserDoesNotExist:
        raise HTTPException(status_code=404)
    except SocialException:
        raise HTTPException(status_code=500)

    return list(map(lambda x: x.dict(), users))
