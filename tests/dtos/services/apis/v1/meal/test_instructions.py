from pydantic import ValidationError
import pytest

from dtos.services.apis.v1.meal.instructions import (
    InstructionsDTO,
    RecipeIngredientDTO,
)

from tests.dtos.services.apis.v1.meal.test_meal_api_dto_abstraction import (
    TestIV1MealAPIServicesDTO,
)


@pytest.mark.asyncio
class TestMealInstructionsServicesDTO(TestIV1MealAPIServicesDTO):

    @pytest.fixture
    def ingredient(self):
        return "test_ingredient"

    @pytest.fixture
    def amount(self):
        return 1

    @pytest.fixture
    def unit(self):
        return "test_unit"

    @pytest.fixture
    def preparation(self):
        return "test_preparation"

    @pytest.fixture
    def description(self):
        return "test_description"

    @pytest.fixture
    def recipe_ingredient(
        self,
        ingredient: str,
        amount: int,
        unit: str,
        preparation: str,
        description: str,
    ):
        return RecipeIngredientDTO(
            ingredient=ingredient,
            amount=amount,
            unit=unit,
            preparation=preparation,
            description=description,
        )

    @pytest.fixture
    def instructions_list(self, recipe_ingredient: RecipeIngredientDTO):
        return [recipe_ingredient]

    async def test_recipe_ingredient_services_dto_all_field_valid(
        self,
        ingredient: str,
        amount: int,
        unit: str,
        preparation: str,
        description: str,
    ):
        recipe_ingredient_services_dto = RecipeIngredientDTO(
                ingredient=ingredient,
                amount=amount,
                unit=unit,
                preparation=preparation,
                description=description,
            )

        assert recipe_ingredient_services_dto.ingredient == ingredient
        assert recipe_ingredient_services_dto.amount == amount
        assert recipe_ingredient_services_dto.unit == unit
        assert recipe_ingredient_services_dto.preparation == preparation
        assert recipe_ingredient_services_dto.description == description

    async def test_instructions_services_dto_all_field_valid(
        self,
        instructions_list,
    ):
        instructions_services_dto = InstructionsDTO(
            instructions=instructions_list,
        )

        assert instructions_services_dto.instructions == instructions_list

    async def test_instructions_services_dto_all_none_error(self):
        with pytest.raises(ValidationError) as exc_info:
            InstructionsDTO(
                instructions=None,
            )
        assert isinstance(exc_info.value.errors(), list)
        assert len(exc_info.value.errors()) == 1
