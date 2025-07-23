from pydantic import BaseModel, Field
from typing import List


class RecipeIngredientDTO(BaseModel):
    ingredient: str = Field(
        ..., description="Name of the ingredient, e.g., 'onion'."
    )
    amount: float = Field(
        ..., description="Amount of the ingredient, e.g., 2.5."
    )
    unit: str = Field(
        ..., description="Unit of measurement, e.g., 'cups', 'grams'."
    )
    preparation: str = Field(
        None,
        description=(
            "Preparation details, e.g., 'chopped', 'diced'. "
        ),
    )


class InstructionsDTO(BaseModel):
    instructions: List[RecipeIngredientDTO] = Field(
        ...,
        description=(
            "List of ingredients and their details for the recipe."
        ),
    )
