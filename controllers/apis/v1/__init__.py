from fastapi import APIRouter
from http import HTTPMethod

from constants.api_lk import APILK

from controllers.apis.v1.meal.add import AddMealController
from controllers.apis.v1.meal.fetch import FetchMealController

from start_utils import logger


router = APIRouter(prefix="/api/v1")

logger.debug(f"Registering {AddMealController.__name__} route.")
router.add_api_route(
    path="/meal/add",
    endpoint=AddMealController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.ADD_MEAL,
)
logger.debug(f"Registered {AddMealController.__name__} route.")


logger.debug(f"Registering {FetchMealController.__name__} route.")
router.add_api_route(
    path="/meal/search",
    endpoint=FetchMealController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.SEARCH_MEAL,
)
logger.debug(f"Registered {FetchMealController.__name__} route.")
