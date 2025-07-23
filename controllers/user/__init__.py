from fastapi import APIRouter
from http import HTTPMethod

from constants.api_lk import APILK

from controllers.user.login import UserLoginController
from controllers.user.register import UserRegistrationController
from controllers.user.logout import UserLogoutController

from start_utils import logger

router = APIRouter(prefix="")

logger.debug(f"Registering {UserLoginController.__name__} route.")
router.add_api_route(
    path="/login",
    endpoint=UserLoginController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.LOGIN,
)
logger.debug(f"Registered {UserLoginController.__name__} route.")

logger.debug(f"Registering {UserRegistrationController.__name__} route.")
router.add_api_route(
    path="/register",
    endpoint=UserRegistrationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.REGISTRATION,
)
logger.debug(f"Registered {UserRegistrationController.__name__} route.")

logger.debug(f"Registering {UserLogoutController.__name__} route.")
router.add_api_route(
    path="/logout",
    endpoint=UserLogoutController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.LOGOUT,
)
logger.debug(f"Registered {UserLogoutController.__name__} route.")
