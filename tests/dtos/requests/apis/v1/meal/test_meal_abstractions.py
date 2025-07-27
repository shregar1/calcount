import pytest

from datetime import datetime

from tests.dtos.requests.apis.v1.test_v1_abstractions import (
    TestIV1APIsRequestDTO,
)


@pytest.mark.asyncio
class TestIV1MealAPIsRequestDTO(TestIV1APIsRequestDTO):

    @pytest.fixture
    def meal_name(self):
        return "test meal"

    @pytest.fixture
    def servings(self):
        return 1

    @pytest.fixture
    def get_instructions_true(self):
        return True

    @pytest.fixture
    def get_instructions_false(self):
        return False

    @pytest.fixture
    def from_date(self):
        return datetime.strptime("2021-01-01", "%Y-%m-%d").date()

    @pytest.fixture
    def to_date(self):
        return datetime.strptime("2021-01-01", "%Y-%m-%d").date()

    @pytest.fixture
    def food_category(self):
        return "keto"
