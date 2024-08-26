from abc import ABCMeta


class RenvooiError(Exception, metaclass=ABCMeta):
    def __init__(self, msg: str):
        self.msg = msg


class RenvooiUnauthorizedError(RenvooiError):
    pass


class RenvooiXmlError(RenvooiError):
    pass


class RenvooiInternalServerError(RenvooiError):
    pass


class RenvooiUnkownError(RenvooiError):
    def __init__(self, msg: str, status_code: int):
        self.msg = msg
        self.status_code = status_code
