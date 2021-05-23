from main import app
from social.constants import RESOURCE_TYPE_TWITTER, RESOURCE_TYPE_VK
from starlette.testclient import TestClient

from .constants import (TWITTER_TEST_USER_ID, TWITTER_WRONG_TEST_USER_ID,
                        VK_TEST_USER_ID, VK_WRONG_TEST_USER_ID)

client = TestClient(app)


def test_get_user_from_vk():
    response = client.get(
        "/api/v1/user/{}".format(VK_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 200


def test_get_articles_from_vk():
    response = client.get(
        "/api/v1/user/{}/article".format(VK_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 200


def test_get_friends_from_vk():
    response = client.get(
        "/api/v1/user/{}/friend".format(VK_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 200


def test_get_follower_from_vk():
    response = client.get(
        "/api/v1/user/{}/follower".format(VK_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 200


def test_get_user_from_vk_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}".format(VK_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 404


def test_get_articles_from_vk_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}/article".format(VK_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 404


def test_get_friends_from_vk_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}/friend".format(VK_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 404


def test_get_follower_from_vk_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}/follower".format(VK_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_VK}
    )
    assert response.status_code == 404


def test_get_user_from_twitter():
    response = client.get(
        "/api/v1/user/{}".format(TWITTER_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 200


def test_get_articles_from_twitter():
    response = client.get(
        "/api/v1/user/{}/article".format(TWITTER_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 200


def test_get_friends_from_twitter():
    response = client.get(
        "/api/v1/user/{}/friend".format(TWITTER_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 200


def test_get_follower_from_twitter():
    response = client.get(
        "/api/v1/user/{}/follower".format(TWITTER_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 200


def test_get_user_from_twitter_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}".format(TWITTER_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 404


def test_get_articles_from_twitter_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}/article".format(TWITTER_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 404


def test_get_friends_from_twitter_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}/friend".format(TWITTER_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 404


def test_get_follower_from_twitter_with_wrong_user_id():
    response = client.get(
        "/api/v1/user/{}/follower".format(TWITTER_WRONG_TEST_USER_ID),
        params={'source': RESOURCE_TYPE_TWITTER}
    )
    assert response.status_code == 404
