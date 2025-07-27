import pytest

from pydantic import ValidationError

from dtos.requests.apis.v1.meal.fetch import FetchMealRequestDTO
from tests.dtos.requests.apis.v1.meal.test_meal_abstractions import (
    TestIV1MealAPIsRequestDTO,
)


@pytest.mark.asyncio
class TestFetchMealRequestDTO(TestIV1MealAPIsRequestDTO):

    async def test_fetch_meal_requests_dto_all_field_valid(
        self,
        reference_number,
        meal_name,
        servings,
        get_instructions_true,
    ):
        request_dto = FetchMealRequestDTO(
            reference_number=reference_number,
            meal_name=meal_name,
            servings=servings,
            get_instructions=get_instructions_true,
        )

        assert request_dto.reference_number == reference_number
        assert request_dto.meal_name == meal_name
        assert request_dto.servings == servings
        assert request_dto.get_instructions == get_instructions_true

    @pytest.mark.parametrize(
        ("field_name", "message_type", "data_type"), [
            ("reference_number", "string", "string_type"),
            ("meal_name", "string", "string_type"),
            ("servings", "integer", "int_type"),
            ("get_instructions", "boolean", "bool_type"),
        ]
    )
    async def test_fetch_meal_parameter_none_error(
        self,
        reference_number,
        meal_name,
        servings,
        get_instructions_true,
        field_name,
        message_type,
        data_type,
        parameter_none_error_factory,
    ):

        reference_number = reference_number
        meal_name = meal_name
        servings = servings
        get_instructions = get_instructions_true

        if field_name == "reference_number":
            reference_number = None
        elif field_name == "meal_name":
            meal_name = None
        elif field_name == "servings":
            servings = None
        else:
            get_instructions = None

        with pytest.raises(ValidationError) as exc_info:

            FetchMealRequestDTO(
                reference_number=reference_number,
                meal_name=meal_name,
                servings=servings,
                get_instructions=get_instructions,
            )

        assert exc_info.value.errors() == parameter_none_error_factory(
            field_name=field_name,
            message_type=message_type,
            data_type=data_type,
        )

    async def test_fetch_meal_requests_dto_all_none_valid(self):

        with pytest.raises(ValidationError) as exc_info:
            FetchMealRequestDTO(
                reference_number=None,
                meal_name=None,
                servings=None,
                get_instructions=None,
            )

        assert isinstance(exc_info.value.errors(), list)
        assert len(exc_info.value.errors()) == 4
        assert exc_info.value.errors()[0]["input"] is None
