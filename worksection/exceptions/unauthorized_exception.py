from .response_exception import ResponseException


class UnauthorizedException(ResponseException):
    def __init__(self, message: str = 'Unauthorized', status_code: int = 401):
        super().__init__(message, status_code)