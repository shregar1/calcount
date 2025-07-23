from fastapi import APIRouter
from http import HTTPMethod

from constants.api_lk import APILK

from controllers.user.admin.login import UserAdminLoginController

from controllers.user.candidate.login import UserCandidateLoginController
from controllers.user.candidate.register import (
    UserCandidateRegisterstionController,
)

from controllers.user.company.login import UserCompanyLoginController
from controllers.user.company.register import (
    UserCompanyRegisterstionController,
)

from controllers.user.employee.login import UserEmployeeLoginController
from controllers.user.employee.register import (
    UserEmployeeRegisterstionController,
)

from controllers.user.employer.login import UserEmployerLoginController
from controllers.user.employer.register import (
    UserEmployerRegisterstionController,
)

from controllers.user.interviewer.login import UserInterviewerLoginController
from controllers.user.interviewer.register import (
    UserInterviewerRegisterstionController,
)

from controllers.user.logout import UserLogoutController

from start_utils import logger

router = APIRouter(prefix="")

logger.debug(f"Registering {UserAdminLoginController.__name__} route.")
router.add_api_route(
    path="/admin/login",
    endpoint=UserAdminLoginController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.ADMIN_LOGIN,
)
logger.debug(f"Registered {UserAdminLoginController.__name__} route.")

logger.debug(
    f"Registering {UserCandidateRegisterstionController.__name__} route."
)
router.add_api_route(
    path="/candidate/register",
    endpoint=UserCandidateRegisterstionController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_REGISTRATION,
)
logger.debug(
    f"Registered {UserCandidateRegisterstionController.__name__} route."
)

logger.debug(f"Registering {UserCandidateLoginController.__name__} route.")
router.add_api_route(
    path="/candidate/login",
    endpoint=UserCandidateLoginController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_LOGIN,
)
logger.debug(f"Registered {UserCandidateLoginController.__name__} route.")

logger.debug(f"Registering {UserCompanyLoginController.__name__} route.")
router.add_api_route(
    path="/company/login",
    endpoint=UserCompanyLoginController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.COMPANY_LOGIN,
)
logger.debug(f"Registered {UserCompanyLoginController.__name__} route.")

logger.debug(
    f"Registering {UserCompanyRegisterstionController.__name__} route."
)
router.add_api_route(
    path="/company/register",
    endpoint=UserCompanyRegisterstionController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.COMPANY_REGISTRATION,
)
logger.debug(
    f"Registered {UserCompanyRegisterstionController.__name__} route."
)

logger.debug(
    f"Registering {UserEmployeeRegisterstionController.__name__} route."
)
router.add_api_route(
    path="/employee/register",
    endpoint=UserEmployeeRegisterstionController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYEE_REGISTRATION,
)
logger.debug(
    f"Registered {UserEmployeeRegisterstionController.__name__} route."
)

logger.debug(f"Registering {UserEmployeeLoginController.__name__} route.")
router.add_api_route(
    path="/employee/login",
    endpoint=UserEmployeeLoginController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYEE_LOGIN,
)
logger.debug(f"Registered {UserEmployeeLoginController.__name__} route.")

logger.debug(
    f"Registering {UserEmployerRegisterstionController.__name__} route."
)
router.add_api_route(
    path="/employer/register",
    endpoint=UserEmployerRegisterstionController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYER_REGISTRATION,
)
logger.debug(
    f"Registered {UserEmployerRegisterstionController.__name__} route."
)

logger.debug(f"Registering {UserEmployerLoginController.__name__} route.")
router.add_api_route(
    path="/employer/login",
    endpoint=UserEmployerLoginController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYER_LOGIN,
)
logger.debug(f"Registered {UserEmployerLoginController.__name__} route.")

logger.debug(
    f"Registering {UserInterviewerRegisterstionController.__name__} route."
)
router.add_api_route(
    path="/interviewer/register",
    endpoint=UserInterviewerRegisterstionController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.INTERVIEWER_REGISTRATION,
)
logger.debug(
    f"Registered {UserInterviewerRegisterstionController.__name__} route."
)

logger.debug(f"Registering {UserInterviewerLoginController.__name__} route.")
router.add_api_route(
    path="/interviewer/login",
    endpoint=UserInterviewerLoginController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.INTERVIEWER_LOGIN,
)
logger.debug(f"Registered {UserInterviewerLoginController.__name__} route.")

logger.debug(f"Registering {UserLogoutController.__name__} route.")
router.add_api_route(
    path="/logout",
    endpoint=UserLogoutController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.LOGOUT,
)
logger.debug(f"Registered {UserLogoutController.__name__} route.")
