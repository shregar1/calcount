"""
DTOs for meal recommendation API responses.
"""
from typing import List
from pydantic import BaseModel, Field


class MealDTO(BaseModel):
    """
    DTO for a single meal recommendation.
    Fields:
        meal_name (str): The name of the meal to recommend.
        servings (int): The number of servings to recommend.
    """
    meal_name: str = Field(
        ...,
        description="The name of the meal to recommend.",
    )
    servings: int = Field(
        ...,
        description="The number of servings to recommend.",
    )


class MealRecommendationDTO(BaseModel):
    """
    DTO for a list of meal recommendations.
    Fields:
        meals (List[MealDTO]): The meals to recommend.
    """
    meals: List[MealDTO] = Field(
        ...,
        description="The meals to recommend.",
    )
