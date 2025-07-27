import json
import requests

from http import HTTPStatus, HTTPMethod
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Any, Dict, List

from constants.meal.nutrients import Nutrients
from constants.meal.prompt.instructions import MealInstructionsPrompt
from constants.meal.prompt.recommendation import MealRecommendationPrompt

from dtos.responses.base import BaseResponseDTO
from dtos.services.apis.v1.meal.instructions import InstructionsDTO
from dtos.services.apis.v1.meal.recommendation import MealRecommendationDTO

from errors.bad_input_error import BadInputError
from errors.not_found_error import NotFoundError
from errors.unexpected_response_error import UnexpectedResponseError

from services.apis.v1.abstraction import IV1APIService

from start_utils import llm


class IMealAPIService(IV1APIService):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: int = None,
    ) -> None:
        super().__init__(urn, user_urn, api_name, user_id)

    def run(self, request_dto: BaseModel) -> BaseResponseDTO:
        pass

    async def make_api_request(
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
                    httpStatusCode=HTTPStatus.NOT_FOUND,
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
                    httpStatusCode=response.status_code,
                )

        except requests.exceptions.HTTPError as e:

            self.logger.error(f"HTTP error: {e}")
            raise BadInputError(
                responseMessage=f"HTTP error occurred: {e}",
                responseKey="error_http_error",
                httpStatusCode=response.status_code,
            )

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise UnexpectedResponseError(
                responseMessage=f"Request failed: {e}",
                responseKey="error_request_failed",
                httpStatusCode=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    async def select_food_record_with_ingredients_and_nutrients(
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

        if len(data) == 0:
            return None

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
        return data[0]

    async def generate_instructions(
        self,
        meal_name: str,
        ingredients: List[Dict]
    ) -> InstructionsDTO:

        parser = PydanticOutputParser(pydantic_object=InstructionsDTO)
        prompt = MealInstructionsPrompt.INSTRUCTIONS_PROMPT.format(
            meal_name=meal_name,
            ingredients=ingredients,
        )
        llm_response = llm.invoke(prompt)
        response: InstructionsDTO = parser.parse(llm_response.content)
        return response

    async def generate_meal_recommendation(
        self,
        food_category: str,
        meal_history: List[Dict[str, Any]]
    ) -> MealRecommendationDTO:

        parser = PydanticOutputParser(pydantic_object=MealRecommendationDTO)
        prompt = MealRecommendationPrompt.MEAL_RECOMMENDATION_PROMPT.format(
            food_category=food_category,
            past_meals_json=json.dumps(meal_history)
        )
        llm_response = llm.invoke(prompt)
        response: MealRecommendationDTO = parser.parse(llm_response.content)
        return response

    async def extract_essential_nutrients(
        self,
        meal_data: dict
    ) -> dict:
        """
        Extracts essential non-zero macronutrients and micronutrients from
        meal data and formats them for human readability, eliminating
        extra details.

        Args:
            meal_data (dict): The 'data' dictionary from the API response.

        Returns:
            dict: A dictionary containing essential nutrient categories.
        """

        essential_macros_list = Nutrients.MACROS_LIST
        essential_micros_list = Nutrients.MICROS_LIST

        extracted_nutrients = {
            "macros": [],
            "micros": []
        }

        for nutrient in meal_data.get("foodNutrients", []):

            name = nutrient.get("nutrientName")
            value = nutrient.get("value")
            unit = nutrient.get("unitName")

            if value is not None and value != 0:

                if name in essential_macros_list:

                    extracted_nutrients["macros"].append(
                        {
                            "name": name,
                            "amount": value,
                            "unit": unit
                        }
                    )

                elif name in essential_micros_list:

                    extracted_nutrients["micros"].append(
                        {
                            "name": name,
                            "amount": value,
                            "unit": unit
                        }
                    )

        return extracted_nutrients

    async def calculate_total_calories(
        self,
        meal_data: dict
    ) -> tuple:
        """
        Calculates the total calories for the meal based on the 'Energy'
        nutrient.

        Args:
            meal_data (dict): The 'data' dictionary from the API response.

        Returns:
            tuple: A tuple containing the total calories and its unit,
            or (None, None) if not found.
        """

        for nutrient in meal_data.get("foodNutrients", []):

            if (
                nutrient.get("nutrientName") == "Energy" and
                nutrient.get("unitName") == "KCAL"
            ):
                return nutrient.get("value"), nutrient.get("unitName")

        return None, None

    async def extract_ingredients(
        self,
        meal_data: dict
    ) -> List[Dict]:

        ingredients = meal_data.get("finalFoodInputFoods", [])

        ingredients_list = []

        for ingredient in ingredients:

            ingredient_name = ingredient.get("foodDescription")
            ingredient_quantity = ingredient.get("gramWeight")
            portion_description = ingredient.get("portionDescription")
            unit = ingredient.get("unit")
            amount = ingredient.get("value")

            ingredients_list.append({
                "name": ingredient_name,
                "quantity_grams": ingredient_quantity,
                "portionDescription": portion_description,
                "amount": amount,
                "unit": unit
            })
        return ingredients_list

    async def process_meal_details(
        self,
        meal_name: str,
        servings: int,
        meal_details: dict,
        get_instructions: bool
    ) -> dict:

        foods_data = meal_details.get("foods", [])

        callable = self.select_food_record_with_ingredients_and_nutrients
        meal_data = await callable(
            data=foods_data
        )

        if not meal_data:
            raise NotFoundError(
                responseMessage="No meal data found",
                responseKey="error_no_meal_data_found",
                httpStatusCode=HTTPStatus.NOT_FOUND,
            )

        total_calories, calories_unit = await self.calculate_total_calories(
            meal_data=meal_data
        )

        essential_nutrients = await self.extract_essential_nutrients(
            meal_data=meal_data
        )

        ingredients = await self.extract_ingredients(
            meal_data=meal_data
        )

        if get_instructions:
            self.logger.info("Instructions requested")
            try:

                self.logger.info("Generating instructions")
                instructions = await self.generate_instructions(
                    meal_name=meal_name,
                    ingredients=ingredients
                )
                instructions = instructions.model_dump().get(
                    "instructions", []
                )
                self.logger.info("Instructions generated")

            except Exception as e:
                self.logger.error(f"Error generating instructions: {e}")
                instructions = []

        else:

            self.logger.info("No instructions requested")
            instructions = []

        return {
            "nutrients": essential_nutrients,
            "ingredients": ingredients,
            "instructions": instructions,
            "total_calories": total_calories,
            "calories_unit": calories_unit
        }
