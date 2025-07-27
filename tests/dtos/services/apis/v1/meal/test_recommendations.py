from pydantic import ValidationError
import pytest


from dtos.services.apis.v1.meal.recommendation import (
    MealDTO,
    MealRecommendationDTO,
)

from tests.dtos.services.apis.v1.meal.test_meal_abstraction import (
    TestIV1MealAPIServicesDTO,
)


@pytest.mark.asyncio
class TestMealRecommendationsServicesDTO(TestIV1MealAPIServicesDTO):

    @pytest.fixture
    def meal_name(self):
        return "test_meal_name"

    @pytest.fixture
    def servings(self):
        return 1

    @pytest.fixture
    def meal(self, meal_name, servings):
        return MealDTO(
            meal_name=meal_name,
            servings=servings,
        )

    @pytest.fixture
    def meal_recommendations_list(self, meal):
        return [meal]

    @pytest.fixture
    def meal_recommendations(
        self,
        meal_name: str,
        servings: int,
    ):
        return MealRecommendationDTO(
            meal_name=meal_name,
            servings=servings,
        )

    async def test_meal_recommendations_services_dto_all_field_valid(
        self,
        meal_recommendations_list,
    ):
        meal_recommendations_dto = MealRecommendationDTO(
            meals=meal_recommendations_list,
        )

        assert (
            meal_recommendations_dto.meals == meal_recommendations_list
        )

    async def test_meal_recommendations_services_dto_all_none_error(
        self,
    ):
        with pytest.raises(ValidationError) as exc_info:
            MealRecommendationDTO(
                meals=None,
            )
        assert isinstance(exc_info.value.errors(), list)
        assert len(exc_info.value.errors()) == 1

    async def test_meal_recommendations_services_dto_all_empty_error(self):
        with pytest.raises(ValidationError) as exc_info:
            MealRecommendationDTO(
                meals=None,
            )
        assert isinstance(exc_info.value.errors(), list)
        assert len(exc_info.value.errors()) == 1
