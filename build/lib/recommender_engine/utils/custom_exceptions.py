class RecommenderEngineException(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        self.message = f"Got {self.__class__.__name__}: {message}"
        self.status_code = status_code


class InputError(RecommenderEngineException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)


class DateParseError(RecommenderEngineException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)
