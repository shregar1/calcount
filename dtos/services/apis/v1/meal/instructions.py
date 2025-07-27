"""
DTOs for representing recipe instructions and ingredients for meal APIs.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class RecipeIngredientDTO(BaseModel):
    """
    DTO for a single recipe ingredient or step.
    Fields:
        ingredient (str, optional): Name of the ingredient.
        amount (float, optional): Amount of the ingredient.
        unit (str, optional): Unit of measurement.
        preparation (str, optional): Preparation details (e.g., chopped).
        description (str, optional): Description of the process step.
    """
    ingredient: Optional[str] = Field(
        ..., description="Name of the ingredient, e.g., 'onion'."
    )
    amount: Optional[float] = Field(
        ..., description="Amount of the ingredient, e.g., 2.5."
    )
    unit: Optional[str] = Field(
        ..., description="Unit of measurement, e.g., 'cups', 'grams'."
    )
    preparation: Optional[str] = Field(
        None,
        description=(
            "Preparation details, e.g., 'chopped', 'diced'. "
        ),
    )
    description: Optional[str] = Field(
        None,
        description=(
            "Description of the process step for the ingredient."
        ),
    )


class InstructionsDTO(BaseModel):
    """
    DTO for a list of recipe instructions (ingredients and steps).
    Fields:
        instructions (List[RecipeIngredientDTO]):
            List of recipe ingredients/steps.
    """
    instructions: List[RecipeIngredientDTO] = Field(
        ...,
        description=(
            "List of ingredients and their details for the recipe."
        ),
    )
