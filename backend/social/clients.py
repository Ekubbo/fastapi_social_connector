import json
from abc import abstractmethod
from typing import List
from urllib.parse import urlencode, urljoin

import httplib2
import oauth2
import requests
from core import settings
from fastapi.logger import logger
from pydantic import ValidationError, parse_obj_as

from .constants import RESOURCE_TYPE_TWITTER, RESOURCE_TYPE_VK
from .exceptions import (AuthorizationError, SocialConnectionError,
                         UnknownError, UserDoesNotExist, WrongResourceType,
                         WrongServerResponse)
from .models import (Article, TwitterArticle, TwitterUser, User, VKArticle,
                     VKUser)


class Client:

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_articles(self, user_id: str, count: int = 10) -> List[Article]:
        pass

    @abstractmethod
    def get_friends(self, user_id: str, count: int = 10) -> List[User]:
        pass

    @abstractmethod
    def get_followers(self, user_id: str, count: int = 10) -> List[User]:
        pass


class TwitterClient(Client):

    api_base_URL = 'https://api.twitter.com/1.1/'

    user_api_url = urljoin(api_base_URL, 'users/lookup.json')
    friends_api_url = urljoin(api_base_URL, 'friends/list.json')
    followers_api_url = urljoin(api_base_URL, 'followers/list.json')
    articles_api_url = urljoin(api_base_URL, 'statuses/user_timeline.json')

    def __init__(self):
        self.consumer_key = settings.TWITTER_API_KEY
        self.consumer_secret = settings.TWITTER_API_SECRET_KEY
        self.access_token = settings.TWITTER_ACCESS_TOKEN
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

        use_proxy_server = getattr(settings, 'USE_PROXY_SERVER', False)
        proxy_server_ip = getattr(settings, 'PROXY_SERVER_IP', '')
        proxy_server_port = getattr(settings, 'PROXY_SERVER_PORT', '')

        if use_proxy_server:
            self.proxy_server_ip = proxy_server_ip
            self.proxy_server_port = proxy_server_port
        else:
            self.proxy_server_ip = None
            self.proxy_server_port = None

    def _get_oauth_client(self) -> oauth2.Client:
        consumer = oauth2.Consumer(key=self.consumer_key,
                                   secret=self.consumer_secret)
        access_token = oauth2.Token(key=self.access_token,
                                    secret=self.access_token_secret)
        if self.proxy_server_ip:
            proxy_info = httplib2.ProxyInfo(
                httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL,
                self.proxy_server_ip,
                int(self.proxy_server_port)
            )
        else:
            proxy_info = None

        return oauth2.Client(consumer, access_token, proxy_info=proxy_info)

    def get_user(self, user_id: str) -> User:

        client = self._get_oauth_client()
        params = {'user_id' if user_id.isnumeric() else 'screen_name': user_id}
        request_url = '{}?{}'.format(self.user_api_url, urlencode(params))

        try:
            response, data = client.request(request_url)
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.warning("TwitterClient.get_user(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info("TwitterClient.get_user(), data = {}".format(data))

        if response.status == 404:
            raise UserDoesNotExist()
        elif response.status == 401:
            raise AuthorizationError()
        elif response.status != 200:
            raise UnknownError()

        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise WrongServerResponse()

        if not data:
            raise UserDoesNotExist()

        try:
            return parse_obj_as(TwitterUser, data[0])
        except ValidationError:
            raise WrongServerResponse()

    def get_articles(self, user_id: str, count: int = 10) -> List[Article]:

        client = self._get_oauth_client()
        params = {
            'user_id' if user_id.isnumeric() else 'screen_name': user_id,
            'count': count,
        }
        request_url = '{}?{}'.format(self.articles_api_url, urlencode(params))

        try:
            response, data = client.request(request_url)
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.warning("TwitterClientt.get_articles(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info("TwitterClient.get_articles(), data = {}".format(data))

        if response.status == 404:
            raise UserDoesNotExist()
        elif response.status == 401:
            raise AuthorizationError()
        elif response.status != 200:
            raise UnknownError()

        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise WrongServerResponse()

        try:
            return parse_obj_as(List[TwitterArticle], data)
        except ValidationError:
            raise WrongServerResponse()

    def get_friends(self, user_id: str, count: int = 10) -> List[User]:

        client = self._get_oauth_client()
        params = {
            'user_id' if user_id.isnumeric() else 'screen_name': user_id,
            'count': count
        }
        request_url = '{}?{}'.format(self.friends_api_url, urlencode(params))

        try:
            response, data = client.request(request_url)
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.warning("TwitterClient.get_friends(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info("TwitterClient.get_friends(), data = {}".format(data))

        if response.status == 404:
            raise UserDoesNotExist()
        elif response.status == 401:
            raise AuthorizationError()
        elif response.status != 200:
            raise UnknownError()

        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise WrongServerResponse()

        try:
            return parse_obj_as(List[TwitterUser], data.get('users', []))
        except ValidationError:
            raise WrongServerResponse()

    def get_followers(self, user_id: str, count: int = 10) -> List[User]:

        client = self._get_oauth_client()
        params = {
            'user_id' if user_id.isnumeric() else 'screen_name': user_id,
            'count': count
        }
        request_url = '{}?{}'.format(self.followers_api_url, urlencode(params))

        try:
            response, data = client.request(request_url)
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.warning("TwitterClient.get_followers(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info("TwitterClient.get_followers(), data = {}".format(data))

        if response.status == 404:
            raise UserDoesNotExist()
        elif response.status == 401:
            raise AuthorizationError()
        elif response.status != 200:
            raise UnknownError()

        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise WrongServerResponse()

        try:
            return parse_obj_as(List[TwitterUser], data.get('users', []))
        except ValidationError:
            raise WrongServerResponse()


class VKClient(Client):

    api_base_URL = 'https://api.vk.com/method/'

    user_api_url = urljoin(api_base_URL, 'users.get')
    wall_api_url = urljoin(api_base_URL, 'wall.get')
    friends_api_url = urljoin(api_base_URL, 'friends.get')
    followers_api_url = urljoin(api_base_URL, 'users.getFollowers')

    def __init__(self):
        self.access_token = getattr(settings, 'VK_ACCESS_TOKEN', None)

        use_proxy_server = getattr(settings, 'USE_PROXY_SERVER', False)
        proxy_server_ip = getattr(settings, 'PROXY_SERVER_IP', '')
        proxy_server_port = getattr(settings, 'PROXY_SERVER_PORT', '')

        if use_proxy_server:
            self.proxies = {
                'http': '{}:{}'.format(proxy_server_ip, proxy_server_port),
                'https': '{}:{}'.format(proxy_server_ip, proxy_server_port),
            }
        else:
            self.proxies = None

    def get_user(self, user_id: str) -> User:
        params = {
            'user_ids': user_id,
            'v': '5.89',
            'access_token': self.access_token,
            'fields': 'followers_count,common_count,photo,screen_name'
        }

        try:
            response = requests.get(
                self.user_api_url, params, proxies=self.proxies
            )
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.warning("VKClient.get_user(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info("VKClient.get_user(), data = {}".format(response.text))

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise WrongServerResponse()

        error = data.get('error', None)
        if error:
            if error.get('error_code', None) in [113, 100, 15, 18, 30]:
                raise UserDoesNotExist()
            elif error.get('error_code', None) in [5, 16]:
                raise AuthorizationError()
            else:
                raise UnknownError()

        data = data.get('response', [])
        if len(data) == 0 or data[0].get('deactivated', None) == "deleted":
            raise UserDoesNotExist()

        try:
            return parse_obj_as(VKUser, data[0])
        except ValidationError:
            raise WrongServerResponse()

    def get_articles(self, user_id: str, count: int = 10) -> List[Article]:

        params = {
            'owner_id': user_id,
            'v': '5.89',
            'access_token': self.access_token,
            'count': count,
        }

        try:
            response = requests.get(
                self.wall_api_url, params, proxies=self.proxies
            )
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.info("VKClient.get_articles(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info("VKClient.get_articles(), data = {}".format(response.text))

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise SocialConnectionError()

        error = data.get('error', None)
        if error:
            if error.get('error_code', None) in [113, 100, 15, 18, 30]:
                raise UserDoesNotExist()
            elif error.get('error_code', None) in [5, 16]:
                raise AuthorizationError()
            else:
                raise UnknownError()

        articles = data.get('response', {}).get('items', [])
        try:
            return parse_obj_as(List[VKArticle], articles)
        except ValidationError:
            raise WrongServerResponse(VKUser)

    def get_friends(self, user_id: str, count: int = 10) -> List[User]:
        params = {
            'user_id': user_id,
            'v': '5.21',
            'access_token': self.access_token,
            'count': count,
            'name_case': 'ins',
            'fields': 'followers_count,common_count,photo,screen_name',
        }

        try:
            response = requests.get(
                self.friends_api_url, params, proxies=self.proxies
            )
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.info("VKClient.get_friends(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info("VKClient.get_friends(), data = {}".format(response.text))

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise WrongServerResponse()

        error = data.get('error', None)
        if error:
            if error.get('error_code', None) in [113, 100, 15, 18, 30]:
                raise UserDoesNotExist()
            elif error.get('error_code', None) in [5, 16]:
                raise AuthorizationError()
            else:
                raise UnknownError()

        data = data.get('response', {}).get('items', [])
        try:
            return parse_obj_as(List[VKUser], data)
        except ValidationError:
            raise WrongServerResponse(VKUser)

    def get_followers(self, user_id: str, count: int = 10) -> List[User]:
        params = {
            'user_id': user_id,
            'v': '5.21',
            'access_token': self.access_token,
            'count': count,
            'name_case': 'ins',
            'fields': 'followers_count,common_count,photo,screen_name',
        }

        try:
            response = requests.get(
                self.followers_api_url, params, proxies=self.proxies
            )
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.info("VKClient.get_followers(), e = {}".format(e))
            raise SocialConnectionError()

        logger.info(
            "VKClient.get_followers(), data = {}".format(response.text)
        )

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise WrongServerResponse()

        error = data.get('error', None)
        if error:
            if error.get('error_code', None) in [113, 100, 15, 18, 30]:
                raise UserDoesNotExist()
            elif error.get('error_code', None) in [5, 16]:
                raise AuthorizationError()
            else:
                raise UnknownError()

        data = data.get('response', {}).get('items', [])
        try:
            return parse_obj_as(List[VKUser], data)
        except ValidationError:
            raise WrongServerResponse(VKUser)


class ClientFactory():

    @staticmethod
    def create_client(resource_type: str) -> Client:

        if resource_type == RESOURCE_TYPE_VK:
            return VKClient()
        elif resource_type == RESOURCE_TYPE_TWITTER:
            return TwitterClient()
        else:
            raise WrongResourceType()
