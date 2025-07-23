from pydantic import BaseModel
import requests

from abc import ABC, abstractmethod
from http import HTTPStatus, HTTPMethod
from typing import Dict, List

from constants.prompt.meal.instructions import MealInstructionsPrompt
from dtos.service.api.meal.instructions import InstructionsDTO

from errors.bad_input_error import BadInputError
from errors.not_found_error import NotFoundError
from errors.unexpected_response_error import UnexpectedResponseError

from start_utils import logger, llm


class IService(ABC):

    def __init__(
        self, urn: str = None, user_urn: str = None, api_name: str = None
    ) -> None:
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.logger = logger.bind(
            urn=self.urn, user_urn=self.user_urn, api_name=self.api_name
        )

    def make_api_request(
        self,
        url: str,
        headers: dict = None,
        payload: dict = None,
        method: HTTPMethod = HTTPMethod.POST,
    ) -> dict:
        try:

            self.logger.info(f"Making {method} request to {url}")
            response = requests.request(
                method, url, headers=headers, json=payload
            )

            if response.status_code == HTTPStatus.NOT_FOUND:
                self.logger.error(f"Not Found: {url}")
                raise NotFoundError(
                    responseMessage=f"Resource not found at {url}",
                    responseKey="error_not_found",
                    http_status_code=HTTPStatus.NOT_FOUND,
                )

            response.raise_for_status()
            try:
                return response.json()
            except Exception as e:
                self.logger.error(
                    f"Failed to parse JSON response: {e}"
                )
                raise UnexpectedResponseError(
                    responseMessage=f"Invalid JSON response from {url}",
                    responseKey="error_invalid_json",
                    http_status_code=response.status_code,
                )

        except requests.exceptions.HTTPError as e:

            self.logger.error(f"HTTP error: {e}")
            raise BadInputError(
                responseMessage=f"HTTP error occurred: {e}",
                responseKey="error_http_error",
                http_status_code=response.status_code,
            )

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise UnexpectedResponseError(
                responseMessage=f"Request failed: {e}",
                responseKey="error_request_failed",
                http_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def select_food_record_with_ingredients_and_nutrients(
        self,
        data: List[Dict]
    ) -> Dict | None:
        """
        Selects the first food record from the USDA API response that has both
        non-empty 'finalFoodInputFoods' (ingredients/components)
        and 'foodNutrients'.

        Args:
            api_response (Dict): The raw JSON response from the USDA
            FoodData Central API.

        Returns:
            Dict | None: The selected food item dictionary if found,
            otherwise None.
        """

        for food_item in data:
            has_ingredients = (
                food_item.get('finalFoodInputFoods')
                and len(food_item['finalFoodInputFoods']) > 0
            )
            has_nutrients = (
                food_item.get('foodNutrients')
                and len(food_item['foodNutrients']) > 0
            )

            if has_ingredients and has_nutrients:
                self.logger.debug(
                    f"Selected food record: {food_item.get('description')} "
                    f"(FDC ID: {food_item.get('fdcId')})"
                )
                return food_item

        self.logger.debug(
            "No food record found with both non-empty"
            "ingredients and nutrients. Returning None."
        )
        return None

    def generate_instructions(
        self,
        meal_name: str,
        ingredients: List[Dict]
    ) -> InstructionsDTO:

        prompt = MealInstructionsPrompt.INSTRUCTIONS_PROMPT.format(
            meal_name=meal_name,
            ingredients=ingredients,
        )

        response: InstructionsDTO = llm.invoke(prompt).with_structured_output(
            InstructionsDTO
        )
        return response

    @abstractmethod
    def run(self, data: BaseModel) -> dict:
        pass
