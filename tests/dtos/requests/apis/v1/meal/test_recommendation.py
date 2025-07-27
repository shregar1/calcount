from pydantic import ValidationError
import pytest

from dtos.requests.apis.v1.meal.recommendation import (
    FetchMealRecommendationRequestDTO,
)

from tests.dtos.requests.apis.v1.meal.test_meal_abstractions import (
    TestIV1MealAPIsRequestDTO,
)


@pytest.mark.asyncio
class TestMealRecommendationRequestDTO(TestIV1MealAPIsRequestDTO):

    async def test_fetch_meal_recommendation_requests_dto_all_field_valid(
        self,
        reference_number,
        food_category,
    ):
        request_dto = FetchMealRecommendationRequestDTO(
            reference_number=reference_number,
            food_category=food_category,
        )

        assert request_dto.reference_number == reference_number
        assert request_dto.food_category == food_category

    @pytest.mark.parametrize(
        ("field_name", "message", "data_type", "url"), [
            (
                "reference_number",
                "Input should be a valid string",
                "string_type",
                "https://errors.pydantic.dev/2.11/v/string_type"
            ),
            (
                "food_category",
                "Value error, food_category is required"
                " and must be a non-empty string.",
                "value_error",
                "https://errors.pydantic.dev/2.11/v/value_error"
            ),
        ]
    )
    async def test_fetch_meal_recommendation_parameter_none_error(
        self,
        reference_number,
        food_category,
        field_name,
        message,
        data_type,
        url,
    ):

        reference_number = reference_number
        food_category = food_category

        if field_name == "reference_number":
            reference_number = None
        elif field_name == "food_category":
            food_category = None

        with pytest.raises(ValidationError) as exc_info:
            FetchMealRecommendationRequestDTO(
                reference_number=reference_number,
                food_category=food_category,
            )

        for error in exc_info.value.errors():
            if "ctx" in error:
                error.pop("ctx")

            assert error["input"] is None
            assert error["loc"] == (field_name,)
            assert error["msg"] == message
            assert error["type"] == data_type
            assert error["url"] == url

    async def test_fetch_meal_recommendation_invalid_food_category_error(
        self,
        reference_number,
    ):

        reference_number = reference_number
        food_category = "abc"

        with pytest.raises(ValidationError) as exc_info:
            FetchMealRecommendationRequestDTO(
                reference_number=reference_number,
                food_category=food_category,
            )

        error = exc_info.value.errors()[0]
        assert error["input"] == "abc"
        assert error["loc"] == ("food_category",)
        assert error["msg"] == "Value error, food_category must be one of: " \
            "keto, vegan, fruitarian, carnivore, paleo"
        assert error["type"] == "value_error"
        assert error["url"] == "https://errors.pydantic.dev/2.11/v/value_error"

    async def test_fetch_meal_recommendation_requests_dto_all_none_valid(self):

        with pytest.raises(ValidationError) as exc_info:
            FetchMealRecommendationRequestDTO(
                reference_number=None,
                food_category=None,
            )

        assert isinstance(exc_info.value.errors(), list)
        assert len(exc_info.value.errors()) == 2
        assert exc_info.value.errors()[0]["input"] is None
