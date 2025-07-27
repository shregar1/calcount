import datetime
import pytest

from unittest.mock import Mock

from constants.api_status import APIStatus

from dtos.requests.apis.v1.meal.history import FetchMealHistoryRequestDTO
from models.meal_log import MealLog

from services.apis.v1.meal.history import FetchMealHistoryService

from tests.services.apis.v1.test_v1_api_service_abstraction import (
    TestIV1APIService,
)


@pytest.mark.asyncio
class TestFetchMealHistoryService(TestIV1APIService):

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
        return Mock()

    @pytest.fixture(autouse=True)
    def setup(
        self,
        urn,
        user_urn,
        api_name,
        user_id,
        meal_log_repository,
    ):
        self.fetch_meal_history_service: FetchMealHistoryService = (
            FetchMealHistoryService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                meal_log_repository=meal_log_repository,
                cache=Mock(),
            )
        )
        self.fetch_meal_history_service.cache.get = Mock(
            return_value='{}'
        )
        self.fetch_meal_history_service.cache.set = Mock(
            return_value=None
        )

    @pytest.fixture
    def valid_fetch_meal_history_data(
        self,
        reference_number,
    ):
        from_date = datetime.date.today() - datetime.timedelta(days=7)
        to_date = datetime.date.today()
        return FetchMealHistoryRequestDTO(
            reference_number=reference_number,
            from_date=from_date,
            to_date=to_date,
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
                created_by=user_id,
            ),
            MealLog(
                id=2,
                urn=urn,
                user_id=user_id,
                meal_name="pasta carbonara",
                servings=1,
                nutrients={"protein": 15, "carbs": 45},
                ingredients=["pasta", "eggs", "cheese"],
                instructions=["Boil pasta", "Mix with eggs"],
                total_calories_per_serving=350,
                calories_unit="kcal",
                total_calories=350,
                is_deleted=False,
                created_on=datetime.datetime.now(),
                created_by=user_id,
            ),
        ]

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

    async def test_successful_fetch_meal_history(
        self,
        valid_fetch_meal_history_data,
        mock_meal_logs,
    ):
        service = self.fetch_meal_history_service
        fn = service.meal_log_repository
        fn.retrieve_history_by_user_id_date_range = Mock(
            return_value=mock_meal_logs
        )

        result = await service.run(request_dto=valid_fetch_meal_history_data)

        fn = service.meal_log_repository
        fn.retrieve_history_by_user_id_date_range.assert_called_once_with(
            user_id=service.user_id,
            from_date=valid_fetch_meal_history_data.from_date,
            to_date=valid_fetch_meal_history_data.to_date,
            is_deleted=False,
        )

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_fetch_meal"
        assert result.responseMessage == (
            "Successfully fetched the meal history."
        )
        assert result.data is not None

        assert isinstance(result.data, dict)
        date_keys = list(result.data.keys())
        assert len(date_keys) == 1

        meals_for_date = result.data[date_keys[0]]
        assert len(meals_for_date) == 2

        first_meal = meals_for_date[0]
        assert first_meal["meal_name"] == mock_meal_logs[0].meal_name
        assert first_meal["servings"] == mock_meal_logs[0].servings
        assert first_meal["nutrients"] == mock_meal_logs[0].nutrients
        assert first_meal["ingredients"] == mock_meal_logs[0].ingredients
        assert first_meal["instructions"] == mock_meal_logs[0].instructions
        assert first_meal["total_calories"] == mock_meal_logs[0].total_calories
        assert first_meal["calories_unit"] == mock_meal_logs[0].calories_unit
        assert first_meal["source"] == "usda"

    async def test_empty_meal_history(
        self,
        valid_fetch_meal_history_data,
    ):
        service = self.fetch_meal_history_service
        fn = service.meal_log_repository
        fn.retrieve_history_by_user_id_date_range = Mock(
            return_value=[]
        )

        result = await service.run(request_dto=valid_fetch_meal_history_data)

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "error_no_meal_history"
        assert result.responseMessage == "No meal history found."
        assert result.data is None

    async def test_single_meal_history(
        self,
        valid_fetch_meal_history_data,
        mock_meal_logs,
    ):
        service = self.fetch_meal_history_service
        single_meal = [mock_meal_logs[0]]
        fn = service.meal_log_repository
        fn.retrieve_history_by_user_id_date_range = Mock(
            return_value=single_meal
        )

        result = await service.run(request_dto=valid_fetch_meal_history_data)

        assert result.status == APIStatus.SUCCESS
        assert result.responseKey == "success_fetch_meal"
        assert result.data is not None

        date_keys = list(result.data.keys())
        assert len(date_keys) == 1
        meals_for_date = result.data[date_keys[0]]
        assert len(meals_for_date) == 1

    async def test_repository_error_handling(
        self,
        valid_fetch_meal_history_data,
    ):
        service = self.fetch_meal_history_service
        fn = service.meal_log_repository
        fn.retrieve_history_by_user_id_date_range = Mock(
            side_effect=Exception("Database error")
        )

        with pytest.raises(Exception) as exc_info:
            await service.run(request_dto=valid_fetch_meal_history_data)

        assert str(exc_info.value) == "Database error"

    async def test_date_range_validation(
        self,
        reference_number,
    ):
        from_date = datetime.date.today()
        to_date = datetime.date.today() - datetime.timedelta(days=1)

        with pytest.raises(ValueError) as exc_info:
            FetchMealHistoryRequestDTO(
                reference_number=reference_number,
                from_date=from_date,
                to_date=to_date,
            )

        assert "to_date cannot be before from_date" in str(exc_info.value)

    async def test_future_date_validation(
        self,
        reference_number,
    ):
        from_date = datetime.date.today()
        to_date = datetime.date.today() + datetime.timedelta(days=1)

        with pytest.raises(ValueError) as exc_info:
            FetchMealHistoryRequestDTO(
                reference_number=reference_number,
                from_date=from_date,
                to_date=to_date,
            )

        assert "to_date cannot be in the future" in str(exc_info.value)

    async def test_default_dates(
        self,
        reference_number,
    ):
        request_dto = FetchMealHistoryRequestDTO(
            reference_number=reference_number,
        )

        service = self.fetch_meal_history_service
        repository = service.meal_log_repository
        repository.retrieve_history_by_user_id_date_range = Mock(
            return_value=[]
        )

        result = await service.run(request_dto=request_dto)

        assert result.status == APIStatus.SUCCESS
        method = repository.retrieve_history_by_user_id_date_range
        method.assert_called_once_with(
            user_id=service.user_id,
            from_date=datetime.date.today(),
            to_date=datetime.date.today(),
            is_deleted=False,
        )

    async def test_meal_history_with_deleted_meals(
        self,
        valid_fetch_meal_history_data,
        mock_meal_logs,
    ):
        service = self.fetch_meal_history_service
        # Add a deleted meal to the list
        deleted_meal = MealLog(
            id=3,
            urn="deleted-urn",
            user_id=service.user_id,
            meal_name="deleted meal",
            servings=1,
            nutrients={},
            ingredients=[],
            instructions=[],
            total_calories_per_serving=100,
            calories_unit="kcal",
            total_calories=100,
            is_deleted=True,
            created_on=datetime.datetime.now(),
            created_by=service.user_id,
        )

        all_meals = mock_meal_logs + [deleted_meal]
        fn = service.meal_log_repository
        fn.retrieve_history_by_user_id_date_range = Mock(
            return_value=all_meals
        )

        result = await service.run(request_dto=valid_fetch_meal_history_data)

        assert result.status == APIStatus.SUCCESS
        assert result.data is not None

        date_keys = list(result.data.keys())
        meals_for_date = result.data[date_keys[0]]
        assert len(meals_for_date) == 3

        meal_names = [meal["meal_name"] for meal in meals_for_date]
        assert "deleted meal" in meal_names

    async def test_multiple_dates_organization(
        self,
        valid_fetch_meal_history_data,
    ):
        service = self.fetch_meal_history_service

        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)

        meal_today = MealLog(
            id=1,
            urn="test-urn",
            user_id=service.user_id,
            meal_name="today meal",
            servings=1,
            nutrients={},
            ingredients=[],
            instructions=[],
            total_calories_per_serving=200,
            calories_unit="kcal",
            total_calories=200,
            is_deleted=False,
            created_on=today,
            created_by=service.user_id,
        )

        meal_yesterday = MealLog(
            id=2,
            urn="test-urn",
            user_id=service.user_id,
            meal_name="yesterday meal",
            servings=1,
            nutrients={},
            ingredients=[],
            instructions=[],
            total_calories_per_serving=300,
            calories_unit="kcal",
            total_calories=300,
            is_deleted=False,
            created_on=yesterday,
            created_by=service.user_id,
        )

        fn = service.meal_log_repository
        fn.retrieve_history_by_user_id_date_range = Mock(
            return_value=[meal_today, meal_yesterday]
        )

        result = await service.run(request_dto=valid_fetch_meal_history_data)

        assert result.status == APIStatus.SUCCESS
        assert result.data is not None

        date_keys = list(result.data.keys())
        assert len(date_keys) == 2

        for date_key in date_keys:
            meals_for_date = result.data[date_key]
            assert len(meals_for_date) == 1
