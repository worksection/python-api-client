from worksection.exception import WorksectionException


class ResponseException(WorksectionException):
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code

    @classmethod
    def from_data(cls, data: dict, status_code: int) -> 'ResponseException':
        message = (
            data.get('errorDescription')
            or data.get('message')
            or ('Unauthorized' if status_code == 401 else 'Failed to fetch data from API')
        )
        return cls(message, status_code)