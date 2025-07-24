from pydantic import BaseModel


class FetchMealRequestDTO(BaseModel):

    meal_name: str
    servings: int
    get_instructions: bool
