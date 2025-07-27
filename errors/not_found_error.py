from abstractions.error import IError


class NotFoundError(IError):

    def __init__(
        self, responseMessage: str, responseKey: str, httpStatusCode: int
    ) -> None:

        super().__init__()
        self.responseMessage = responseMessage
        self.responseKey = responseKey
        self.httpStatusCode = httpStatusCode
