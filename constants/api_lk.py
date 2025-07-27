"""
API Logical Keys (APILK) constants for identifying API operations.
"""
from typing import Final


class APILK:
    """
    Logical keys for API operations, used for routing and identification.
    """
    LOGIN: Final[str] = "LOGIN"
    REGISTRATION: Final[str] = "REGISTRATION"
    LOGOUT: Final[str] = "LOGOUT"
    CREATE_PROFILE: Final[str] = "CREATE_PROFILE"
    SEARCH_MEAL: Final[str] = "SEARCH_MEAL"
    ADD_MEAL: Final[str] = "ADD_MEAL"
    MEAL_HISTORY: Final[str] = "MEAL_HISTORY"
    MEAL_RECOMMENDATION: Final[str] = "MEAL_RECOMMENDATION"
