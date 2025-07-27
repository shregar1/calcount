import datetime
import pytest

from http import HTTPStatus
from unittest.mock import Mock, AsyncMock

from constants.api_status import APIStatus

from errors.unexpected_response_error import UnexpectedResponseError
from models.meal_log import MealLog

from tests.services.apis.v1.meal.test_v1_meal_api_abstraction import (
    TestIV1MealAPIService
)


@pytest.mark.asyncio
class TestAddMealService(TestIV1MealAPIService):

    @pytest.fixture
    def mock_meal_log(
        self,
        urn,
        user_id,
        meal_name,
        servings,
        nutrients,
        ingredients,
        instructions,
        total_calories_per_serving,
        calories_unit,
    ):
        return MealLog(
            id=1,
            urn=urn,
            user_id=user_id,
            meal_name=meal_name,
            servings=servings,
            nutrients=nutrients,
            ingredients=ingredients,
            instructions=instructions,
            total_calories_per_serving=total_calories_per_serving,
            calories_unit=calories_unit,
            total_calories=total_calories_per_serving*servings,
            is_deleted=False,
            created_on=datetime.datetime.now(),
            created_by=user_id
        )

    async def test_successful_add_meal_with_instructions(
        self,
        valid_add_meal_data_with_instructions,
        meal_name,
        servings,
        nutrients,
        ingredients,
        instructions,
        total_calories_per_serving,
        calories_unit,
        mock_meal_log,
    ):
        service = self.add_meal_service
        service.make_api_request = AsyncMock(
            return_value={}
        )
        service.process_meal_details = AsyncMock(
            return_value={
                "meal_name": meal_name,
                "servings": servings,
                "nutrients": nutrients,
                "ingredients": ingredients,
                "instructions": instructions,
                "total_calories": total_calories_per_serving,
                "calories_unit": calories_unit
            }
        )
        service.meal_log_repository.create_record = Mock(
            return_value=mock_meal_log
        )

        result = await service.run(
            request_dto=valid_add_meal_data_with_instructions
        )

        service.meal_log_repository.create_record.assert_called_once()
        service.make_api_request.assert_awaited_once()
        service.process_meal_details.assert_awaited_once()

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_add_meal"
        assert result.responseMessage == "Successfully added the meal."
        assert result.data["meal_name"] == meal_name
        assert result.data["servings"] == servings
        assert isinstance(result.data["nutrients_per_serving"], dict)
        assert isinstance(result.data["ingredients_per_serving"], list)
        assert isinstance(result.data["instructions_per_serving"], list)
        assert result.data["total_calories_per_serving"] == (
            total_calories_per_serving
        )
        assert result.data["calories_unit"] == calories_unit
        assert result.data["total_calories"] == (
            total_calories_per_serving*servings
        )
        assert result.data["source"] == "usda"

    async def test_successful_add_meal_without_instructions(
        self,
        valid_add_meal_data_without_instructions,
        meal_name,
        servings,
        nutrients,
        ingredients,
        instructions,
        total_calories_per_serving,
        calories_unit,
        mock_meal_log,
    ):
        service = self.add_meal_service
        service.make_api_request = AsyncMock(
            return_value={}
        )
        service.process_meal_details = AsyncMock(
            return_value={
                "meal_name": meal_name,
                "servings": servings,
                "nutrients": nutrients,
                "ingredients": ingredients,
                "instructions": instructions,
                "total_calories": total_calories_per_serving,
                "calories_unit": calories_unit
            }
        )
        service.meal_log_repository.create_record = Mock(
            return_value=mock_meal_log
        )

        result = await service.run(
            request_dto=valid_add_meal_data_without_instructions
        )

        service.meal_log_repository.create_record.assert_called_once()
        service.make_api_request.assert_awaited_once()
        service.process_meal_details.assert_awaited_once()

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_add_meal"
        assert result.responseMessage == "Successfully added the meal."
        assert result.data["meal_name"] == meal_name
        assert result.data["servings"] == servings
        assert isinstance(result.data["nutrients_per_serving"], dict)
        assert isinstance(result.data["ingredients_per_serving"], list)
        assert result.data["instructions_per_serving"] == []
        assert result.data["total_calories_per_serving"] == (
            total_calories_per_serving
        )
        assert result.data["calories_unit"] == calories_unit
        assert result.data["total_calories"] == (
            total_calories_per_serving*servings
        )
        assert result.data["source"] == "usda"

    async def test_negative_calories(
        self,
        valid_add_meal_data_with_instructions,
    ):

        service = self.add_meal_service
        service.make_api_request = AsyncMock(return_value={})
        service.process_meal_details = AsyncMock(return_value={
            "meal_name": "test",
            "servings": 1,
            "nutrients": {},
            "ingredients": [],
            "instructions": [],
            "total_calories": -100,
            "calories_unit": "kcal"
        })
        service.meal_log_repository.create_record = AsyncMock()

        with pytest.raises(UnexpectedResponseError) as exc_info:
            await service.run(
                request_dto=valid_add_meal_data_with_instructions
            )

        assert exc_info.value.httpStatusCode == (
            HTTPStatus.UNPROCESSABLE_ENTITY
        )
        assert exc_info.value.responseMessage == (
            "Calories cannot be negative."
        )
        assert exc_info.value.responseKey == "error_negative_calories"
