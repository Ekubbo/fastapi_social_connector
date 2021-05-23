from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    screen_name: str
    name: str
    followers_count: int
    friends_count: int
    image_url: str
    description: str


class VKUser(User):
    name: str = Field(alias='first_name')
    friends_count: str = Field(alias='followers_count', default=0)
    followers_count: str = Field(alias='common_count', default=0)
    image_url: str = Field(alias='photo')
    description: str = ''


class TwitterUser(User):
    image_url: str = Field(alias='profile_image_url')


class Article(BaseModel):
    id: int
    text: str
    likes_count: int
    comments_count: int
    reposts_count: int
    retweet_count: int


class TwitterArticle(Article):
    likes_count: int = Field(alias='favorite_count')
    comments_count: int = 0
    reposts_count: int = 0


class VKArticle(Article):
    likes_count: int = Field(alias='likes__count', default=0)
    comments_count: int = Field(alias='comments.count', default=0)
    reposts_count: int = Field(alias='reposts.count', default=0)
    retweet_count: int = 0

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.likes_count =  data.get('likes', {}).get('count', 0)
        self.comments_count =  data.get('comments', {}).get('count', 0)
        self.reposts_count = data.get('reposts', {}).get('count', 0)
