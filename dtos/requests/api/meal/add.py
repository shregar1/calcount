from pydantic import BaseModel


class AddMealRequestDTO(BaseModel):

    meal_name: str
    servings: int
