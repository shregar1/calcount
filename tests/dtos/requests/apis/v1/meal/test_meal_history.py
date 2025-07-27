import pytest

from pydantic import ValidationError

from dtos.requests.apis.v1.meal.history import FetchMealHistoryRequestDTO

from tests.dtos.requests.apis.v1.meal.test_meal_abstractions import (
    TestIV1MealAPIsRequestDTO,
)


@pytest.mark.asyncio
class TestMealHistoryRequestDTO(TestIV1MealAPIsRequestDTO):

    async def test_fetch_meal_history_requests_dto_all_field_valid(
        self,
        reference_number,
        from_date,
        to_date,
    ):
        request_dto = FetchMealHistoryRequestDTO(
            reference_number=reference_number,
            from_date=from_date,
            to_date=to_date,
        )

        assert request_dto.reference_number == reference_number
        assert request_dto.from_date == from_date
        assert request_dto.to_date == to_date

    @pytest.mark.parametrize(
        ("field_name", "error_type", "error_message"), [
            (
                "reference_number",
                "string_type",
                "Input should be a valid string",
            ),
            (
                "from_date",
                "value_error",
                "Value error, from_date is required.",
            ),
            (
                "to_date",
                "value_error",
                "Value error, to_date is required.",
            ),
        ]
    )
    async def test_fetch_meal_parameter_none_error(
        self,
        reference_number,
        from_date,
        to_date,
        field_name,
        error_type,
        error_message,
    ):

        reference_number = reference_number
        from_date = from_date
        to_date = to_date

        if field_name == "reference_number":
            reference_number = None
        elif field_name == "from_date":
            from_date = None
        elif field_name == "to_date":
            to_date = None

        with pytest.raises(ValidationError) as exc_info:

            FetchMealHistoryRequestDTO(
                reference_number=reference_number,
                from_date=from_date,
                to_date=to_date,
            )

        for error in exc_info.value.errors():
            assert error["type"] == error_type
            assert error["loc"] == (field_name,)
            assert error["msg"] == error_message
            assert error["input"] is None
            assert error["url"] == (
                f"https://errors.pydantic.dev/2.11/v/{error_type}"
            )

    async def test_fetch_meal_history_requests_dto_all_none_valid(
        self,
    ):

        with pytest.raises(ValidationError) as exc_info:
            FetchMealHistoryRequestDTO(
                reference_number=None,
                from_date=None,
                to_date=None,
            )

        assert isinstance(exc_info.value.errors(), list)
        assert len(exc_info.value.errors()) == 3
        assert exc_info.value.errors()[0]["type"] == "string_type"
        assert exc_info.value.errors()[0]["msg"] == (
            "Input should be a valid string"
        )
        assert exc_info.value.errors()[0]["input"] is None
        assert exc_info.value.errors()[0]["url"] == (
            "https://errors.pydantic.dev/2.11/v/string_type"
        )
