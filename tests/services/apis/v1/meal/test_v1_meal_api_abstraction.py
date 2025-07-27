import json
import pytest
from unittest.mock import AsyncMock, Mock, patch

from dtos.requests.apis.v1.meal.add import AddMealRequestDTO
from dtos.services.apis.v1.meal.instructions import (
    InstructionsDTO,
    RecipeIngredientDTO,
)
from dtos.services.apis.v1.meal.recommendation import MealRecommendationDTO

from errors.not_found_error import NotFoundError
from errors.unexpected_response_error import UnexpectedResponseError

from repositories.meal_log import MealLogRepository

from services.apis.v1.meal.add import AddMealService

from tests.services.apis.v1.test_v1_api_service_abstraction import (
    TestIV1APIService
)


@pytest.mark.asyncio
class TestIV1MealAPIService(TestIV1APIService):

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
    def source(self):
        """
        Source.
        """
        return "usda"

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
    def meal_data(self):
        """
        Meal data.
        """
        return {
            "finalFoodInputFoods": [
                {
                    "foodDescription": "ingredient1",
                    "gramWeight": 100,
                    "id": 1,
                    "portionCode": "0",
                    "portionDescription": "description",
                    "unit": "piece",
                    "rank": 9,
                    "retentionCode": 3460,
                    "srCode": 11282,
                    "value": 100
                },
                {
                    "foodDescription": "ingredient2",
                    "gramWeight": 50,
                    "id": 2,
                    "portionCode": "0",
                    "portionDescription": "description",
                    "unit": "piece",
                    "rank": 9,
                    "retentionCode": 3460,
                    "srCode": 11282,
                    "value": 50
                },
            ],
            "foodNutrients": [
                {
                    "nutrientId": 1005,
                    "nutrientName": "Carbohydrate, by difference",
                    "nutrientNumber": "205",
                    "unitName": "G",
                    "derivationCode": "LCCS",
                    "derivationDescription": "description",
                    "derivationId": 70,
                    "value": 18.6,
                    "foodNutrientSourceId": 9,
                    "foodNutrientSourceCode": "12",
                    "foodNutrientSourceDescription": "description",
                    "rank": 1110,
                    "indentLevel": 2,
                    "foodNutrientId": 26240784,
                    "percentDailyValue": 20
                },
                {
                    "nutrientId": 1008,
                    "nutrientName": "Energy",
                    "nutrientNumber": "208",
                    "unitName": "KCAL",
                    "derivationCode": "LCCS",
                    "derivationDescription": "description",
                    "derivationId": 70,
                    "value": 140,
                    "foodNutrientSourceId": 9,
                    "foodNutrientSourceCode": "12",
                    "foodNutrientSourceDescription": "description",
                    "rank": 300,
                    "indentLevel": 1,
                    "foodNutrientId": 26240785
                },
                {
                    "nutrientId": 1087,
                    "nutrientName": "Calcium, Ca",
                    "nutrientNumber": "301",
                    "unitName": "MG",
                    "derivationCode": "LCCD",
                    "derivationDescription": "description",
                    "derivationId": 75,
                    "value": 18.0,
                    "foodNutrientSourceId": 9,
                    "foodNutrientSourceCode": "12",
                    "foodNutrientSourceDescription": "description",
                    "rank": 5300,
                    "indentLevel": 1,
                    "foodNutrientId": 26240788,
                    "percentDailyValue": 6
                }
            ]
        }

    @pytest.fixture
    def meal_details(self, meal_data):
        """
        Meal details.
        """
        return [
            {
                "description": "Food 1",
                "fdcId": 1,
                "finalFoodInputFoods": meal_data["finalFoodInputFoods"],
                "foodNutrients": meal_data["foodNutrients"]
            },
            {
                "description": "Food 2",
                "fdcId": 2,
                "finalFoodInputFoods": meal_data["finalFoodInputFoods"],
                "foodNutrients": meal_data["foodNutrients"]
            }
        ]

    @pytest.fixture
    def meal_instructions(self):
        """
        Meal instructions.
        """
        return [
            {
                "ingredient": "ingredient",
                "amount": 1.0,
                "unit": "unit",
                "preparation": None,
                "description": "description"
            }
        ]

    @pytest.fixture
    def meal_recommendation(self):
        """
        Meal recommendation.
        """
        return [
                {
                    "meal_name": "meal name",
                    "servings": 2
                }
            ]

    @pytest.fixture(autouse=True)
    def setup(
        self,
        urn,
        user_urn,
        api_name,
        meal_log_repository,
    ):
        self.meal_log_repository: MealLogRepository = meal_log_repository
        self.add_meal_service = AddMealService(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            meal_log_repository=self.meal_log_repository,
        )

    @pytest.fixture
    def valid_add_meal_data_with_instructions(
        self,
        reference_number,
        meal_name,
        servings,
        get_instructions_true,
    ):
        return AddMealRequestDTO(
            reference_number=reference_number,
            meal_name=meal_name,
            servings=servings,
            get_instructions=get_instructions_true
        )

    @pytest.fixture
    def valid_add_meal_data_without_instructions(
        self,
        reference_number,
        meal_name,
        servings,
        get_instructions_false,
    ):
        return AddMealRequestDTO(
            reference_number=reference_number,
            meal_name=meal_name,
            servings=servings,
            get_instructions=get_instructions_false
        )

    @patch('services.apis.v1.meal.abstraction.requests.request')
    async def test_make_api_request_success(self, mock_request):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"foods": []}
        mock_request.return_value = mock_response

        result = await self.add_meal_service.make_api_request(
            url="https://api.nal.usda.gov/fdc/v1/foods/search",
            method="GET",
            headers={"x-api-key": "test-key"}
        )

        assert result == {"foods": []}
        mock_request.assert_called_once()

    @patch('services.apis.v1.meal.abstraction.requests.request')
    async def test_make_api_request_not_found(self, mock_request):
        """Test API request with 404 response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response

        with pytest.raises(NotFoundError) as exc_info:
            await self.add_meal_service.make_api_request(
                url="https://api.nal.usda.gov/fdc/v1/foods/search",
                method="GET"
            )

        assert exc_info.value.responseKey == "error_not_found"

    @patch('services.apis.v1.meal.abstraction.requests.request')
    async def test_make_api_request_http_error(self, mock_request):
        """Test API request with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_request.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            await self.add_meal_service.make_api_request(
                url="https://api.nal.usda.gov/fdc/v1/foods/search",
                method="GET"
            )

        assert exc_info.value.args[0] == "HTTP Error"

    @patch('services.apis.v1.meal.abstraction.requests.request')
    async def test_make_api_request_invalid_json(self, mock_request):
        """Test API request with invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Exception("Invalid JSON")
        mock_request.return_value = mock_response

        with pytest.raises(UnexpectedResponseError) as exc_info:
            await self.add_meal_service.make_api_request(
                url="https://api.nal.usda.gov/fdc/v1/foods/search",
                method="GET"
            )

        assert exc_info.value.responseKey == "error_invalid_json"

    @patch('services.apis.v1.meal.abstraction.requests.request')
    async def test_make_api_request_connection_error(self, mock_request):
        """Test API request with connection error."""
        mock_request.side_effect = Exception("Connection failed")

        with pytest.raises(Exception) as exc_info:
            await self.add_meal_service.make_api_request(
                url="https://api.nal.usda.gov/fdc/v1/foods/search",
                method="GET"
            )

        assert exc_info.value.args[0] == "Connection failed"

    async def test_select_food_record_with_ingredients_and_nutrients_success(
        self
    ):
        """Test successful food record selection."""
        data = [
            {
                "description": "Food 1",
                "fdcId": 1,
                "finalFoodInputFoods": [{"name": "ingredient1"}],
                "foodNutrients": [{"name": "nutrient1"}]
            },
            {
                "description": "Food 2",
                "fdcId": 2,
                "finalFoodInputFoods": [],
                "foodNutrients": []
            }
        ]

        service = self.add_meal_service
        callable = service.select_food_record_with_ingredients_and_nutrients
        result = await callable(data)

        assert result["description"] == "Food 1"
        assert result["fdcId"] == 1

    @patch('services.apis.v1.meal.abstraction.llm')
    async def test_generate_instructions_success(
        self,
        mock_llm,
        meal_instructions,
    ):
        """Test successful instruction generation."""
        mock_response = Mock()
        mock_response.content = json.dumps(
            {
                "instructions": meal_instructions
            }
        )
        mock_llm.invoke.return_value = mock_response

        ingredients = [{"name": "chicken", "quantity_grams": 100}]

        result = await self.add_meal_service.generate_instructions(
            meal_name="chicken biryani",
            ingredients=ingredients
        )

        assert isinstance(result, InstructionsDTO)
        assert result.instructions[0].model_dump() == meal_instructions[0]

    @patch('services.apis.v1.meal.abstraction.llm')
    async def test_generate_instructions_failure(self, mock_llm):
        """Test instruction generation failure."""
        mock_llm.invoke.side_effect = Exception("LLM Error")

        ingredients = [{"name": "chicken", "quantity_grams": 100}]

        with pytest.raises(Exception) as exc_info:
            await self.add_meal_service.generate_instructions(
                meal_name="chicken biryani",
                ingredients=ingredients
            )

        assert "LLM Error" in str(exc_info.value)

    @patch('services.apis.v1.meal.abstraction.llm')
    async def test_generate_meal_recommendation_success(
        self,
        mock_llm,
        meal_recommendation,
    ):
        """Test successful meal recommendation generation."""
        mock_response = Mock()
        mock_response.content = json.dumps(
            {
                "meals": meal_recommendation
            }
        )
        mock_llm.invoke.return_value = mock_response

        meal_history = [{"meal_name": "pasta", "calories": 300}]

        result = await self.add_meal_service.generate_meal_recommendation(
            food_category="keto",
            meal_history=meal_history
        )

        assert isinstance(result, MealRecommendationDTO)
        assert result.meals[0].model_dump() == meal_recommendation[0]

    @patch('services.apis.v1.meal.abstraction.llm')
    async def test_generate_meal_recommendation_failure(self, mock_llm):
        """Test meal recommendation generation failure."""
        mock_llm.invoke.side_effect = Exception("LLM Error")

        meal_history = [{"meal_name": "pasta", "calories": 300}]

        with pytest.raises(Exception) as exc_info:
            await self.add_meal_service.generate_meal_recommendation(
                food_category="lunch",
                meal_history=meal_history
            )

        assert "LLM Error" in str(exc_info.value)

    async def test_extract_essential_nutrients_success(self, meal_data: dict):
        """Test successful nutrient extraction."""

        result = await self.add_meal_service.extract_essential_nutrients(
            meal_data=meal_data
        )

        assert "macros" in result
        assert "micros" in result
        assert len(result["macros"]) > 0
        assert len(result["micros"]) > 0

    async def test_extract_essential_nutrients_empty_data(self):
        """Test nutrient extraction with empty data."""
        meal_data = {"foodNutrients": []}

        result = await self.add_meal_service.extract_essential_nutrients(
            meal_data=meal_data
        )

        assert result["macros"] == []
        assert result["micros"] == []

    async def test_extract_essential_nutrients_zero_values(self):
        """Test nutrient extraction with zero values."""
        meal_data = {
            "foodNutrients": [
                {
                    "nutrientName": "Protein",
                    "value": 0,
                    "unitName": "G"
                },
                {
                    "nutrientName": "Energy",
                    "value": None,
                    "unitName": "KCAL"
                }
            ]
        }

        result = await self.add_meal_service.extract_essential_nutrients(
            meal_data=meal_data
        )

        assert result["macros"] == []
        assert result["micros"] == []

    async def test_calculate_total_calories_success(self):
        """Test successful calorie calculation."""
        meal_data = {
            "foodNutrients": [
                {
                    "nutrientName": "Energy",
                    "value": 250,
                    "unitName": "KCAL"
                },
                {
                    "nutrientName": "Protein",
                    "value": 20,
                    "unitName": "G"
                }
            ]
        }

        calories, unit = await self.add_meal_service.calculate_total_calories(
            meal_data=meal_data
        )

        assert calories == 250
        assert unit == "KCAL"

    async def test_calculate_total_calories_not_found(self):
        """Test calorie calculation when energy not found."""
        meal_data = {
            "foodNutrients": [
                {
                    "nutrientName": "Protein",
                    "value": 20,
                    "unitName": "G"
                }
            ]
        }

        calories, unit = await self.add_meal_service.calculate_total_calories(
            meal_data=meal_data
        )

        assert calories is None
        assert unit is None

    async def test_calculate_total_calories_wrong_unit(self):
        """Test calorie calculation with wrong unit."""
        meal_data = {
            "foodNutrients": [
                {
                    "nutrientName": "Energy",
                    "value": 250,
                    "unitName": "KJ"
                }
            ]
        }

        calories, unit = await self.add_meal_service.calculate_total_calories(
            meal_data=meal_data
        )

        assert calories is None
        assert unit is None

    async def test_extract_ingredients_success(self):
        """Test successful ingredient extraction."""
        meal_data = {
            "finalFoodInputFoods": [
                {
                    "foodDescription": "Chicken",
                    "gramWeight": 100,
                    "portionDescription": "1 piece",
                    "unit": "piece",
                    "value": 1
                },
                {
                    "foodDescription": "Rice",
                    "gramWeight": 50,
                    "portionDescription": "1 cup",
                    "unit": "cup",
                    "value": 1
                }
            ]
        }

        result = await self.add_meal_service.extract_ingredients(meal_data)

        assert len(result) == 2
        assert result[0]["name"] == "Chicken"
        assert result[0]["quantity_grams"] == 100
        assert result[1]["name"] == "Rice"
        assert result[1]["quantity_grams"] == 50

    async def test_extract_ingredients_empty_data(self):
        """Test ingredient extraction with empty data."""
        meal_data = {"finalFoodInputFoods": []}

        result = await self.add_meal_service.extract_ingredients(meal_data)

        assert result == []

    async def test_extract_ingredients_missing_fields(self):
        """Test ingredient extraction with missing fields."""
        meal_data = {
            "finalFoodInputFoods": [
                {
                    "foodDescription": "Chicken",
                }
            ]
        }

        result = await self.add_meal_service.extract_ingredients(meal_data)

        assert len(result) == 1
        assert result[0]["name"] == "Chicken"
        assert result[0]["quantity_grams"] is None

    async def test_process_meal_details_success_with_instructions(self):
        """Test successful meal details processing with instructions."""
        meal_details = {
            "foods": [
                {
                    "description": "Chicken Biryani",
                    "fdcId": 1,
                    "finalFoodInputFoods": [{"foodDescription": "Chicken"}],
                    "foodNutrients": [
                        {
                            "nutrientName": "Energy",
                            "value": 300,
                            "unitName": "KCAL"
                        }
                    ]
                }
            ]
        }

        with (
            patch.object(
                self.add_meal_service,
                'generate_instructions'
            ) as mock_gen,
        ):
            mock_gen.return_value = InstructionsDTO(
                instructions=[RecipeIngredientDTO(
                    ingredient="ingredient",
                    amount=1.0,
                    unit="unit",
                    preparation=None,
                    description="description."
                )]
            )

            result = await self.add_meal_service.process_meal_details(
                meal_name="chicken biryani",
                servings=2,
                meal_details=meal_details,
                get_instructions=True
            )

        assert "nutrients" in result
        assert "ingredients" in result
        assert "instructions" in result
        assert "total_calories" in result
        assert "calories_unit" in result
        assert result["total_calories"] == 300
        assert result["calories_unit"] == "KCAL"

    async def test_process_meal_details_success_without_instructions(self):
        """Test successful meal details processing without instructions."""
        meal_details = {
            "foods": [
                {
                    "description": "Chicken Biryani",
                    "fdcId": 1,
                    "finalFoodInputFoods": [{"foodDescription": "Chicken"}],
                    "foodNutrients": [
                        {
                            "nutrientName": "Energy",
                            "value": 300,
                            "unitName": "KCAL"
                        }
                    ]
                }
            ]
        }

        result = await self.add_meal_service.process_meal_details(
            meal_name="chicken biryani",
            servings=2,
            meal_details=meal_details,
            get_instructions=False
        )

        assert "nutrients" in result
        assert "ingredients" in result
        assert "instructions" in result
        assert result["instructions"] == []

    async def test_process_meal_details_no_food_data(self):
        """Test meal details processing with no food data."""
        meal_details = {"foods": []}

        with pytest.raises(NotFoundError) as exc_info:
            await self.add_meal_service.process_meal_details(
                meal_name="chicken biryani",
                servings=2,
                meal_details=meal_details,
                get_instructions=False
            )

        assert exc_info.value.responseKey == "error_no_meal_data_found"

    async def test_process_meal_details_instructions_generation_failure(self):
        """Test meal details processing when instruction generation fails."""
        meal_details = {
            "foods": [
                {
                    "description": "Chicken Biryani",
                    "fdcId": 1,
                    "finalFoodInputFoods": [{"foodDescription": "Chicken"}],
                    "foodNutrients": [
                        {
                            "nutrientName": "Energy",
                            "value": 300,
                            "unitName": "KCAL"
                        }
                    ]
                }
            ]
        }

        with (
            patch.object(
                self.add_meal_service,
                'generate_instructions'
            ) as mock_gen,
        ):
            mock_gen.side_effect = Exception("LLM Error")

            result = await self.add_meal_service.process_meal_details(
                meal_name="chicken biryani",
                servings=2,
                meal_details=meal_details,
                get_instructions=True
            )

        assert result["instructions"] == []

    async def test_api_request_failure(
        self,
        valid_add_meal_data_with_instructions,
    ):
        service = self.add_meal_service
        service.make_api_request = AsyncMock(
            side_effect=Exception("API error")
        )
        service.process_meal_details = AsyncMock()
        service.meal_log_repository.create_record = AsyncMock()

        with pytest.raises(Exception) as exc_info:
            await service.run(
                request_dto=valid_add_meal_data_with_instructions
            )
        assert "API error" in str(exc_info.value)

    async def test_process_meal_details_failure(
        self,
        valid_add_meal_data_with_instructions,
    ):
        service = self.add_meal_service
        service.make_api_request = AsyncMock(return_value={})
        service.process_meal_details = AsyncMock(
            side_effect=Exception("Parse error")
        )
        service.meal_log_repository.create_record = AsyncMock()

        with pytest.raises(Exception) as exc_info:
            await service.run(
                request_dto=valid_add_meal_data_with_instructions
            )
        assert "Parse error" in str(exc_info.value)
