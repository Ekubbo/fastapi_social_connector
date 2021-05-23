class SocialException(Exception):
    pass


class WrongResourceType(SocialException):
    pass


class WrongServerResponse(SocialException):
    pass


class UserDoesNotExist(SocialException):
    pass


class AuthorizationError(SocialException):
    pass


class UnknownError(SocialException):
    pass


class SocialConnectionError(SocialException):
    pass
