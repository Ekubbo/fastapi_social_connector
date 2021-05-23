from typing import List

from .clients import ClientFactory
from .constants import RESOURCE_TYPES
from .exceptions import SocialException, UserDoesNotExist
from .models import Article, User


def get_user(user_id: str, resource_type: str = None) -> User:

    if resource_type:
        client = ClientFactory.create_client(resource_type)
        return client.get_user(user_id)

    for resource_type in RESOURCE_TYPES:
        client = ClientFactory.create_client(resource_type)
        try:
            user = client.get_user(user_id)
            return user
        except UserDoesNotExist:
            continue
    else:
        raise UserDoesNotExist()


def get_articles(
    user_id: str, count: int, resource_type: str = None
) -> List[Article]:

    if resource_type:
        client = ClientFactory.create_client(resource_type)
        return client.get_articles(user_id, count)

    for resource_type in RESOURCE_TYPES:
        client = ClientFactory.create_client(resource_type)
        try:
            articles = client.get_articles(user_id, count)
            return articles
        except SocialException:
            continue
    else:
        raise UserDoesNotExist()


def get_friends(
    user_id: str, count: int = 10, resource_type: str = None
) -> List[User]:

    if resource_type:
        client = ClientFactory.create_client(resource_type)
        return client.get_friends(user_id, count)

    for resource_type in RESOURCE_TYPES:
        client = ClientFactory.create_client(resource_type)
        try:
            users = client.get_friends(user_id, count)
            return users
        except SocialException:
            continue
    else:
        raise UserDoesNotExist()


def get_followers(
    user_id: str, count: int = 10, resource_type: str = None
) -> List[User]:

    if resource_type:
        client = ClientFactory.create_client(resource_type)
        return client.get_followers(user_id, count)

    for resource_type in RESOURCE_TYPES:
        client = ClientFactory.create_client(resource_type)
        try:
            users = client.get_followers(user_id, count)
            return users
        except SocialException:
            continue
    else:
        raise UserDoesNotExist()
