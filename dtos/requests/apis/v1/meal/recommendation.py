"""
DTO for fetch meal recommendation request payload, with validation for
food category.
"""
from typing import Optional
from pydantic import field_validator
from constants.meal.category import MealCategory
from dtos.requests.abstraction import IRequestDTO


class FetchMealRecommendationRequestDTO(IRequestDTO):
    """
    DTO for fetch meal recommendation request.
    Fields:
        food_category (str, optional): Food category (validated).
    """
    food_category: Optional[str] = None

    @field_validator('food_category')
    @classmethod
    def validate_food_category(cls, v):
        if not v or not str(v).strip():
            raise ValueError(
                "food_category is required and must be a non-empty string."
            )
        allowed = [
            MealCategory.KETO,
            MealCategory.VEGAN,
            MealCategory.FRUITARIAN,
            MealCategory.CARNIVORE,
            MealCategory.PALEO,
        ]
        if v not in allowed:
            raise ValueError(
                f"food_category must be one of: {', '.join(allowed)}"
            )
        return v
