"""
DTO for add meal request payload, with validation for meal name and servings.
"""
from pydantic import field_validator

from dtos.requests.abstraction import IRequestDTO


class AddMealRequestDTO(IRequestDTO):
    """
    DTO for add meal request.
    Fields:
        meal_name (str): Name of the meal (validated).
        servings (int): Number of servings (validated).
        get_instructions (bool): Whether to fetch instructions.
    """
    meal_name: str
    servings: int
    get_instructions: bool

    @field_validator('meal_name')
    @classmethod
    def validate_meal_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Dish name cannot be empty.')
        if len(v.strip()) == 1:
            raise ValueError('Dish name must be more than one character.')
        if len(v) > 100:
            raise ValueError('Dish name is too long (max 100 characters).')
        if any(char.isdigit() for char in v):
            raise ValueError('Dish name cannot contain numbers.')
        if not v.replace(' ', '').isalpha():
            raise ValueError(
                'Dish name must only contain alphabetic characters and spaces.'
            )
        return v

    @field_validator('servings')
    @classmethod
    def validate_servings(cls, v):
        if not isinstance(v, int):
            raise ValueError('Servings must be an integer.')
        if v < 1:
            raise ValueError('Servings must be at least 1.')
        if v > 100:
            raise ValueError('Servings is too large (max 100).')
        return v
