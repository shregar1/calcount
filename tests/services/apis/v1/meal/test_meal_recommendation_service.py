import datetime
import pytest

from unittest.mock import Mock, AsyncMock

from constants.api_status import APIStatus
from constants.meal.category import MealCategory

from dtos.requests.apis.v1.meal.recommendation import (
    FetchMealRecommendationRequestDTO
)
from dtos.services.apis.v1.meal.recommendation import MealRecommendationDTO
from models.meal_log import MealLog
from repositories.meal_log import MealLogRepository

from services.apis.v1.meal.recommendation import FetchMealRecommendationService

from tests.services.apis.v1.test_v1_api_service_abstraction import (
    TestIV1APIService
)


@pytest.mark.asyncio
class TestFetchMealRecommendationService(TestIV1APIService):

    @pytest.fixture(autouse=True)
    def setup(
        self,
        urn,
        user_urn,
        api_name,
        user_id,
        meal_log_repository,
    ):
        self.fetch_meal_recommendation_service = (
            FetchMealRecommendationService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
            )
        )

    @pytest.fixture
    def valid_fetch_meal_recommendation_data(
        self,
        reference_number,
    ):
        return FetchMealRecommendationRequestDTO(
            reference_number=reference_number,
            food_category=MealCategory.KETO,
        )

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

    @pytest.fixture
    def mock_meal_logs(
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
        return [
            MealLog(
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
                total_calories=total_calories_per_serving * servings,
                is_deleted=False,
                created_on=datetime.datetime.now(),
                created_by=user_id
            ),
            MealLog(
                id=2,
                urn=urn,
                user_id=user_id,
                meal_name="keto chicken salad",
                servings=1,
                nutrients={"protein": 25, "fat": 15},
                ingredients=["chicken", "avocado", "olive oil"],
                instructions=["Grill chicken", "Mix ingredients"],
                total_calories_per_serving=300,
                calories_unit="kcal",
                total_calories=300,
                is_deleted=False,
                created_on=datetime.datetime.now(),
                created_by=user_id
            )
        ]

    @pytest.fixture
    def mock_meal_recommendation_dto(self):
        from dtos.services.apis.v1.meal.recommendation import MealDTO
        return MealRecommendationDTO(
            meals=[
                MealDTO(
                    meal_name="Keto Avocado Toast",
                    servings=2
                ),
                MealDTO(
                    meal_name="Keto Salmon Bowl",
                    servings=1
                )
            ]
        )

    async def test_successful_fetch_meal_recommendation(
        self,
        valid_fetch_meal_recommendation_data,
        mock_meal_logs,
        mock_meal_recommendation_dto,
    ):
        service = self.fetch_meal_recommendation_service
        service.meal_log_repository.retrieve_history_by_user_id = (
            Mock(return_value=mock_meal_logs)
        )
        service.process_meal_recommendation = AsyncMock(
            return_value=mock_meal_recommendation_dto
        )

        result = await service.run(
            request_dto=valid_fetch_meal_recommendation_data
        )

        fn = service.meal_log_repository.retrieve_history_by_user_id
        fn.assert_called_once_with(
            user_id=service.user_id,
            is_deleted=False
        )
        service.process_meal_recommendation.assert_awaited_once_with(
            meal_history=mock_meal_logs,
            food_category=MealCategory.KETO
        )

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_fetch_meal_recommendation"
        assert result.responseMessage == (
            "Successfully fetched meal recommendations."
        )
        assert result.data["recommendations"] == (
            mock_meal_recommendation_dto.recommendations
        )
        assert result.data["category"] == MealCategory.KETO
        assert result.data["total_recommendations"] == 2

    async def test_empty_meal_history_recommendation(
        self,
        valid_fetch_meal_recommendation_data,
        mock_meal_recommendation_dto,
    ):
        service = self.fetch_meal_recommendation_service
        service.meal_log_repository.retrieve_history_by_user_id = (
            Mock(return_value=[])
        )
        service.process_meal_recommendation = AsyncMock(
            return_value=mock_meal_recommendation_dto
        )

        result = await service.run(
            request_dto=valid_fetch_meal_recommendation_data
        )

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_fetch_meal_recommendation"
        assert result.responseMessage == (
            "Successfully fetched meal recommendations."
        )
        assert result.data["recommendations"] == (
            mock_meal_recommendation_dto.recommendations
        )

    async def test_different_food_categories(
        self,
        reference_number,
        mock_meal_logs,
        mock_meal_recommendation_dto,
    ):
        categories = [
            MealCategory.VEGAN,
            MealCategory.FRUITARIAN,
            MealCategory.CARNIVORE,
            MealCategory.PALEO,
        ]

        for category in categories:
            request_dto = FetchMealRecommendationRequestDTO(
                reference_number=reference_number,
                food_category=category,
            )

            service = self.fetch_meal_recommendation_service
            service.meal_log_repository.retrieve_history_by_user_id = (
                Mock(return_value=mock_meal_logs)
            )
            service.process_meal_recommendation = AsyncMock(
                return_value=mock_meal_recommendation_dto
            )

            result = await service.run(request_dto=request_dto)

            assert result.status == APIStatus.SUCCESS
            assert result.data["category"] == category
            service.process_meal_recommendation.assert_awaited_with(
                meal_history=mock_meal_logs,
                food_category=category
            )

    async def test_repository_error_handling(
        self,
        valid_fetch_meal_recommendation_data,
    ):
        service = self.fetch_meal_recommendation_service
        service.meal_log_repository.retrieve_history_by_user_id = (
            Mock(side_effect=Exception("Database error"))
        )

        with pytest.raises(Exception) as exc_info:
            await service.run(
                request_dto=valid_fetch_meal_recommendation_data
            )

        assert str(exc_info.value) == "Database error"

    async def test_process_meal_recommendation_error(
        self,
        valid_fetch_meal_recommendation_data,
        mock_meal_logs,
    ):
        service = self.fetch_meal_recommendation_service
        service.meal_log_repository.retrieve_history_by_user_id = (
            Mock(return_value=mock_meal_logs)
        )
        service.process_meal_recommendation = AsyncMock(
            side_effect=Exception("Processing error")
        )

        with pytest.raises(Exception) as exc_info:
            await service.run(
                request_dto=valid_fetch_meal_recommendation_data
            )

        assert str(exc_info.value) == "Processing error"

    async def test_invalid_food_category_validation(
        self,
        reference_number,
    ):
        with pytest.raises(ValueError) as exc_info:
            FetchMealRecommendationRequestDTO(
                reference_number=reference_number,
                food_category="invalid_category",
            )

        assert "food_category must be one of:" in str(exc_info.value)

    async def test_empty_food_category_validation(
        self,
        reference_number,
    ):
        with pytest.raises(ValueError) as exc_info:
            FetchMealRecommendationRequestDTO(
                reference_number=reference_number,
                food_category="",
            )

        assert "food_category is required" in str(exc_info.value)

    async def test_none_food_category_validation(
        self,
        reference_number,
    ):
        with pytest.raises(ValueError) as exc_info:
            FetchMealRecommendationRequestDTO(
                reference_number=reference_number,
                food_category=None,
            )

        assert "food_category is required" in str(exc_info.value)

    async def test_process_meal_recommendation_method(
        self,
        mock_meal_logs,
        mock_meal_recommendation_dto,
    ):
        service = self.fetch_meal_recommendation_service
        service.generate_meal_recommendation = Mock(
            return_value=mock_meal_recommendation_dto
        )

        result = await service.process_meal_recommendation(
            meal_history=mock_meal_logs,
            food_category=MealCategory.KETO
        )

        service.generate_meal_recommendation.assert_called_once_with(
            food_category=MealCategory.KETO,
            meal_history=[
                {
                    "meal_name": mock_meal_logs[0].meal_name,
                    "servings": mock_meal_logs[0].servings,
                    "nutrients": mock_meal_logs[0].nutrients,
                    "ingredients": mock_meal_logs[0].ingredients,
                },
                {
                    "meal_name": mock_meal_logs[1].meal_name,
                    "servings": mock_meal_logs[1].servings,
                    "nutrients": mock_meal_logs[1].nutrients,
                    "ingredients": mock_meal_logs[1].ingredients,
                }
            ]
        )

        assert result == mock_meal_recommendation_dto

    async def test_meal_history_data_transformation(
        self,
        mock_meal_logs,
        mock_meal_recommendation_dto,
    ):
        service = self.fetch_meal_recommendation_service
        service.generate_meal_recommendation = Mock(
            return_value=mock_meal_recommendation_dto
        )

        await service.process_meal_recommendation(
            meal_history=mock_meal_logs,
            food_category=MealCategory.VEGAN
        )

        # Verify the meal history data is correctly transformed
        expected_meal_history = [
            {
                "meal_name": mock_meal_logs[0].meal_name,
                "servings": mock_meal_logs[0].servings,
                "nutrients": mock_meal_logs[0].nutrients,
                "ingredients": mock_meal_logs[0].ingredients,
            },
            {
                "meal_name": mock_meal_logs[1].meal_name,
                "servings": mock_meal_logs[1].servings,
                "nutrients": mock_meal_logs[1].nutrients,
                "ingredients": mock_meal_logs[1].ingredients,
            }
        ]

        service.generate_meal_recommendation.assert_called_once_with(
            food_category=MealCategory.VEGAN,
            meal_history=expected_meal_history
        )

    async def test_recommendation_with_complex_meal_data(
        self,
        valid_fetch_meal_recommendation_data,
        mock_meal_recommendation_dto,
    ):
        # Test with complex meal data including nested structures
        complex_meal_logs = [
            MealLog(
                id=1,
                urn="complex-urn",
                user_id=123,
                meal_name="complex keto meal",
                servings=2,
                nutrients={
                    "protein": {"value": 25, "unit": "g"},
                    "fat": {"value": 30, "unit": "g"},
                    "carbs": {"value": 5, "unit": "g"}
                },
                ingredients=[
                    {"name": "chicken", "amount": "200g"},
                    {"name": "avocado", "amount": "1 whole"},
                    {"name": "olive oil", "amount": "2 tbsp"}
                ],
                instructions=["Step 1", "Step 2", "Step 3"],
                total_calories_per_serving=450,
                calories_unit="kcal",
                total_calories=900,
                is_deleted=False,
                created_on=datetime.datetime.now(),
                created_by=123
            )
        ]

        service = self.fetch_meal_recommendation_service
        service.meal_log_repository.retrieve_history_by_user_id = (
            Mock(return_value=complex_meal_logs)
        )
        service.process_meal_recommendation = AsyncMock(
            return_value=mock_meal_recommendation_dto
        )

        result = await service.run(
            request_dto=valid_fetch_meal_recommendation_data
        )

        assert result.status == APIStatus.SUCCESS
        assert result.data["recommendations"] == (
            mock_meal_recommendation_dto.recommendations
        )
