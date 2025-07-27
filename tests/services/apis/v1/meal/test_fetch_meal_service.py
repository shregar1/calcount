import pytest

from http import HTTPStatus
from unittest.mock import AsyncMock

from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.fetch import FetchMealRequestDTO
from errors.unexpected_response_error import UnexpectedResponseError

from services.apis.v1.meal.fetch import FetchMealService

from tests.services.apis.v1.test_v1_api_service_abstraction import (
    TestIV1APIService
)
from repositories.meal_log import MealLogRepository


@pytest.mark.asyncio
class TestFetchMealService(TestIV1APIService):

    @pytest.fixture
    def meal_name(self):
        """
        Meal name.
        """
        return "chicken biryani"

    @pytest.fixture
    def servings(self):
        """
        Servings.
        """
        return 2

    @pytest.fixture
    def get_instructions_true(self):
        """
        Get instructions true.
        """
        return True

    @pytest.fixture
    def get_instructions_false(self):
        """
        Get instructions false.
        """
        return False

    @pytest.fixture
    def nutrients(self):
        """
        Nutrients.
        """
        return dict()

    @pytest.fixture
    def ingredients(self):
        """
        Ingredients.
        """
        return list()

    @pytest.fixture
    def instructions(self):
        """
        Instructions.
        """
        return list()

    @pytest.fixture
    def total_calories_per_serving(self):
        """
        Total calories per serving.
        """
        return 240

    @pytest.fixture
    def calories_unit(self):
        """
        Calories unit.
        """
        return "kcal"

    @pytest.fixture
    def meal_log_repository(
        self,
        urn,
        user_urn,
        api_name,
        user_id,
        db_session,
    ):
        """
        Meal Log repository.
        """
        return MealLogRepository(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            session=db_session,
            user_id=user_id,
        )

    @pytest.fixture(autouse=True)
    def setup(
        self,
        urn,
        user_urn,
        api_name,
        meal_log_repository,
    ):
        self.fetch_meal_service: FetchMealService = FetchMealService(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            meal_log_repository=meal_log_repository,
        )

    @pytest.fixture
    def valid_fetch_meal_data_with_instructions(
        self,
        reference_number,
        meal_name,
        servings,
        get_instructions_true,
    ):
        return FetchMealRequestDTO(
            reference_number=reference_number,
            meal_name=meal_name,
            servings=servings,
            get_instructions=get_instructions_true,
        )

    @pytest.fixture
    def valid_fetch_meal_data_without_instructions(
        self,
        reference_number,
        meal_name,
        servings,
        get_instructions_false,
    ):
        return FetchMealRequestDTO(
            reference_number=reference_number,
            meal_name=meal_name,
            servings=servings,
            get_instructions=get_instructions_false,
        )

    async def test_successful_fetch_meal_with_instructions(
        self,
        valid_fetch_meal_data_with_instructions,
        meal_name,
        servings,
        nutrients,
        ingredients,
        instructions,
        total_calories_per_serving,
        calories_unit,
    ):
        service = self.fetch_meal_service
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

        result = await service.run(
            request_dto=valid_fetch_meal_data_with_instructions
        )

        service.make_api_request.assert_awaited_once()
        service.process_meal_details.assert_awaited_once()

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_fetch_meal"
        assert result.responseMessage == (
            "Successfully fetched the meal details."
        )
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
            total_calories_per_serving * servings
        )

    async def test_successful_fetch_meal_without_instructions(
        self,
        valid_fetch_meal_data_without_instructions,
        meal_name,
        servings,
        nutrients,
        ingredients,
        total_calories_per_serving,
        calories_unit,
    ):
        service = self.fetch_meal_service
        service.make_api_request = AsyncMock(
            return_value={}
        )
        service.process_meal_details = AsyncMock(
            return_value={
                "meal_name": meal_name,
                "servings": servings,
                "nutrients": nutrients,
                "ingredients": ingredients,
                "total_calories": total_calories_per_serving,
                "calories_unit": calories_unit
            }
        )

        result = await service.run(
            request_dto=valid_fetch_meal_data_without_instructions
        )

        service.make_api_request.assert_awaited_once()
        service.process_meal_details.assert_awaited_once()

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_fetch_meal"
        assert result.responseMessage == (
            "Successfully fetched the meal details."
        )
        assert result.data["meal_name"] == meal_name
        assert result.data["servings"] == servings
        assert isinstance(result.data["nutrients_per_serving"], dict)
        assert isinstance(result.data["ingredients_per_serving"], list)
        assert result.data["instructions_per_serving"] is None
        assert result.data["total_calories_per_serving"] == (
            total_calories_per_serving
        )
        assert result.data["calories_unit"] == calories_unit
        assert result.data["total_calories"] == (
            total_calories_per_serving * servings
        )

    async def test_api_request_failure(
        self,
        valid_fetch_meal_data_with_instructions,
    ):
        service = self.fetch_meal_service
        service.make_api_request = AsyncMock(
            side_effect=UnexpectedResponseError(
                responseMessage="External API error",
                responseKey="error_external_api",
                httpStatusCode=HTTPStatus.BAD_GATEWAY
            )
        )

        with pytest.raises(UnexpectedResponseError) as exc_info:
            await service.run(
                request_dto=valid_fetch_meal_data_with_instructions
            )

        assert exc_info.value.responseKey == "error_external_api"
        assert exc_info.value.responseMessage == "External API error"
        assert exc_info.value.httpStatusCode == HTTPStatus.BAD_GATEWAY

    async def test_process_meal_details_failure(
        self,
        valid_fetch_meal_data_with_instructions,
    ):
        service = self.fetch_meal_service
        service.make_api_request = AsyncMock(return_value={})
        service.process_meal_details = AsyncMock(
            side_effect=UnexpectedResponseError(
                responseMessage="Meal processing error",
                responseKey="error_meal_processing",
                httpStatusCode=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        )

        with pytest.raises(UnexpectedResponseError) as exc_info:
            await service.run(
                request_dto=valid_fetch_meal_data_with_instructions
            )

        assert exc_info.value.responseKey == "error_meal_processing"
        assert exc_info.value.responseMessage == "Meal processing error"
        assert exc_info.value.httpStatusCode == (
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

    async def test_zero_calories_handling(
        self,
        valid_fetch_meal_data_with_instructions,
        meal_name,
        servings,
        nutrients,
        ingredients,
        instructions,
    ):
        service = self.fetch_meal_service
        service.make_api_request = AsyncMock(return_value={})
        service.process_meal_details = AsyncMock(
            return_value={
                "meal_name": meal_name,
                "servings": servings,
                "nutrients": nutrients,
                "ingredients": ingredients,
                "instructions": instructions,
                "total_calories": 0,
                "calories_unit": "kcal"
            }
        )

        result = await service.run(
            request_dto=valid_fetch_meal_data_with_instructions
        )

        assert result.status == APIStatus.SUCCESS
        assert result.data["total_calories_per_serving"] == 0
        assert result.data["total_calories"] == 0

    async def test_large_servings_calculation(
        self,
        valid_fetch_meal_data_with_instructions,
        meal_name,
        nutrients,
        ingredients,
        instructions,
        total_calories_per_serving,
        calories_unit,
        reference_number
    ):
        large_servings = 10
        request_dto = FetchMealRequestDTO(
            reference_number=reference_number,
            meal_name=meal_name,
            servings=large_servings,
            get_instructions=True,
        )

        service = self.fetch_meal_service
        service.make_api_request = AsyncMock(return_value={})
        service.process_meal_details = AsyncMock(
            return_value={
                "meal_name": meal_name,
                "servings": large_servings,
                "nutrients": nutrients,
                "ingredients": ingredients,
                "instructions": instructions,
                "total_calories": total_calories_per_serving,
                "calories_unit": calories_unit
            }
        )

        result = await service.run(request_dto=request_dto)

        assert result.status == APIStatus.SUCCESS
        assert result.data["servings"] == large_servings
        assert result.data["total_calories"] == (
            total_calories_per_serving * large_servings
        )

    async def test_different_calorie_units(
        self,
        valid_fetch_meal_data_with_instructions,
        meal_name,
        servings,
        nutrients,
        ingredients,
        instructions,
        total_calories_per_serving,
    ):
        service = self.fetch_meal_service
        service.make_api_request = AsyncMock(return_value={})
        service.process_meal_details = AsyncMock(
            return_value={
                "meal_name": meal_name,
                "servings": servings,
                "nutrients": nutrients,
                "ingredients": ingredients,
                "instructions": instructions,
                "total_calories": total_calories_per_serving,
                "calories_unit": "cal"
            }
        )

        result = await service.run(
            request_dto=valid_fetch_meal_data_with_instructions
        )

        assert result.status == APIStatus.SUCCESS
        assert result.data["calories_unit"] == "cal"
        assert result.data["total_calories_per_serving"] == (
            total_calories_per_serving
        )

    async def test_empty_nutrients_and_ingredients(
        self,
        valid_fetch_meal_data_with_instructions,
        meal_name,
        servings,
        instructions,
        total_calories_per_serving,
        calories_unit,
    ):
        service = self.fetch_meal_service
        service.make_api_request = AsyncMock(return_value={})
        service.process_meal_details = AsyncMock(
            return_value={
                "meal_name": meal_name,
                "servings": servings,
                "nutrients": {},
                "ingredients": [],
                "instructions": instructions,
                "total_calories": total_calories_per_serving,
                "calories_unit": calories_unit
            }
        )

        result = await service.run(
            request_dto=valid_fetch_meal_data_with_instructions
        )

        assert result.status == APIStatus.SUCCESS
        assert result.data["nutrients_per_serving"] == {}
        assert result.data["ingredients_per_serving"] == []
        assert result.data["instructions_per_serving"] == instructions
