from typing import List
from pydantic import BaseModel, Field


class MealDTO(BaseModel):
    meal_name: str = Field(
        ...,
        description="The name of the meal to recommend.",
    )
    servings: int = Field(
        ...,
        description="The number of servings to recommend.",
    )


class MealRecommendationDTO(BaseModel):
    meals: List[MealDTO] = Field(
        ...,
        description="The meals to recommend.",
    )
