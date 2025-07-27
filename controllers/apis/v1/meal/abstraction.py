from controllers.apis.v1.abstraction import IV1APIController


class IV1MealAPIController(IV1APIController):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
    ) -> None:
        super().__init__(urn, user_urn, api_name, user_id)
        pass
