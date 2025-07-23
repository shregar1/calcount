from typing import Final


class MealInstructionsPrompt:

    INSTRUCTIONS_PROMPT: Final[str] = """
    You are a helpful assistant that generates instructions for a meal.
    The meal is {meal_name} and the ingredients are {ingredients}.
    """
