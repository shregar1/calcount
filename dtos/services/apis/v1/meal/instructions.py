from pydantic import BaseModel, Field
from typing import List, Optional


class RecipeIngredientDTO(BaseModel):
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
    instructions: List[RecipeIngredientDTO] = Field(
        ...,
        description=(
            "List of ingredients and their details for the recipe."
        ),
    )
