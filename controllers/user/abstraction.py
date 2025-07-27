from abstractions.controller import IController


class IUserController(IController):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
    ) -> None:
        super().__init__(urn, user_urn, api_name, user_id)
        pass
