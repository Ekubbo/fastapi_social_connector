from enum import Enum
from social.models import User, Article
from social.constants import RESOURCE_TYPE_VK, RESOURCE_TYPE_TWITTER


class Source(str, Enum):
    VKONTAKTE = RESOURCE_TYPE_VK
    TWITTER = RESOURCE_TYPE_TWITTER
