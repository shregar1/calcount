from http import HTTPMethod, HTTPStatus

from abstractions.service import IService

from constants.api_status import APIStatus

from dtos.requests.api.meal.add import AddMealRequestDTO
from dtos.responses.base import BaseResponseDTO

from dtos.service.api.meal.instructions import InstructionsDTO
from errors.not_found_error import NotFoundError

from repositories.meal_log import MealLogRepository

from start_utils import USDA_API_KEY, usda_configuration


class FetchMealService(IService):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
        meal_log_repository: MealLogRepository = None
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.user_id = user_id
        self.meal_log_repository = meal_log_repository

    def process_meal_details(
        self,
        meal_name: str,
        meal_details: dict
    ) -> dict:

        foods_data = meal_details.get("foods", [])

        meal_data = self.select_food_record_with_ingredients_and_nutrients(
            data=foods_data
        )

        if not meal_data:
            raise NotFoundError(
                responseMessage="No meal data found",
                responseKey="error_no_meal_data_found",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )

        nutrients = meal_data.get("foodNutrients")
        ingredients = meal_data.get("foodIngredients")

        instructions_dto: InstructionsDTO = self.generate_instructions(
            meal_name=meal_name,
            ingredients=ingredients
        )

        return {
            "nutrients": nutrients,
            "ingredients": ingredients,
            "instructions": instructions_dto.model_dump().get(
                "instructions", [{}]
            ),
        }

    async def run(self, request_dto: AddMealRequestDTO) -> BaseResponseDTO:

        self.logger.info("Fetching meal details")
        url = usda_configuration.url.format(
                query=request_dto.meal_name,
                api_key=USDA_API_KEY
            )
        meal_details = self.make_api_request(
            url=url,
            method=HTTPMethod.GET,
            headers=self.headers,
            payload=request_dto.model_dump()
        )
        self.logger.info("Meal details fetched")

        self.logger.info("Parsing meal details")
        meal_data = self.process_meal_details(meal_details)
        self.logger.info("Meal details parsed")

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Successfully fetched the meal details.",
            responseKey="success_fetch_meal",
            data={
                "meal_name": request_dto.meal_name,
                "servings": request_dto.servings,
                "nutrients": meal_data.get("nutrients"),
                "ingredients": meal_data.get("ingredients"),
                "instructions": meal_data.get("instructions"),
            },
        )
