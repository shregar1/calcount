from fastapi import APIRouter
from http import HTTPMethod

from constants.api_lk import APILK

from controllers.apis.chat.create import ChatCreateController
from controllers.apis.chat.fetch import ChatFetchUserChatsController

from controllers.apis.candidate.application.create import (
    CandidateCreateJobApplicationController,
)
from controllers.apis.candidate.application.fetch_all import (
    CandidateFetchJobApplicationsController,
)
from controllers.apis.candidate.application.fetch import (
    CandidateFetchJobApplicationController,
)

from controllers.apis.candidate.interview.session.fetch import (
    CandidateFetchInterviewController,
)
from controllers.apis.candidate.interview.request.create import (
    CandidateCreateInterviewRequestController,
)

from controllers.apis.candidate.job.fetch_all import (
    CandidateFetchJobsController,
)
from controllers.apis.candidate.job.fetch import CandidateFetchJobController

from controllers.apis.candidate.profile.create import (
    CandidateCreateProfileController,
)

from controllers.apis.candidate.profile.education_qualification.add import (
    CandidateAddEducationQualificationController,
)
from controllers.apis.candidate.profile.education_qualification.delete import (
    CandidateDeleteEducationQualificationController,
)

from controllers.apis.candidate.profile.fetch import (
    CandidateFetchProfileController,
)
from controllers.apis.candidate.profile.fetch_all import (
    CandidateFetchProfilesController,
)

from controllers.apis.candidate.profile.project.add import (
    CandidateAddProjectController,
)
from controllers.apis.candidate.profile.project.delete import (
    CandidateDeleteProjectController,
)

from controllers.apis.candidate.profile.skill.add import (
    CandidateAddSkillController,
)
from controllers.apis.candidate.profile.skill.delete import (
    CandidateDeleteSkillController,
)

from controllers.apis.candidate.profile.work_experience.add import (
    CandidateAddWorkExperienceController,
)
from controllers.apis.candidate.profile.work_experience.delete import (
    CandidateDeleteWorkExperienceController,
)

from controllers.apis.company.application.recommendation.fetch import (
    CompanyFetchRecommendedApplicationsController,
)

from controllers.apis.company.employer.fetch import (
    CompanyFetchEmployersController,
)
from controllers.apis.company.employer.onboarding import (
    CompanyEmployerOnboardingEmailController,
)

from controllers.apis.company.profile.fetch import (
    CompanyFetchCompanyController,
)
from controllers.apis.company.profile.fetch_all import (
    CompanyFetchallController,
)

from controllers.apis.company.job.fetch import (
    CompanyFetchCompanyJobsController,
)

from controllers.apis.currency.fetch import CurrencyFetchAllController

from controllers.apis.employee.application.fetch import (
    EmployeeFetchJobApplicationsController,
)
from controllers.apis.employee.application.recommend import (
    EmployeeRecommendApplicationController,
)
from controllers.apis.employee.application.reviewed import (
    EmployeeReviewedApplicationController,
)
from controllers.apis.employee.profile.fetch import (
    EmployeeFetchProfileController,
)
from controllers.apis.employee.company.job.fetch import (
    EmployeeFetchCompanyJobsController,
)


from controllers.apis.employer.application.accept import (
    EmployerAcceptApplicationController,
)
from controllers.apis.employer.application.fetch import (
    EmployerFetchJobApplicationsController,
)
from controllers.apis.employer.application.hire import (
    EmployerHireApplicationController,
)
from controllers.apis.employer.application.recommendation.fetch import (
    EmployerFetchRecommendedApplicationsController,
)

from controllers.apis.employer.profile.create import (
    EmployerCreateProfileController,
)
from controllers.apis.employer.profile.fetch import (
    EmployerFetchProfileController,
)

from controllers.apis.employer.job.create import EmployerCreateJobController
from controllers.apis.employer.job.delete import EmployerDeletJobController

from controllers.apis.employer.job.fetch import (
    EmployerFetchEmployerJobsController,
)
from controllers.apis.employer.application.reject import (
    EmployerRejectApplicationController,
)
from controllers.apis.employer.application.update import (
    EmployerUpdateApplicationProgressController,
)

from controllers.apis.interviewer.interview.request.fetch import (
    InterviewerFetchInterviewRequestsController,
)
from controllers.apis.interviewer.interview.session.fetch import (
    InterviewerFetchInterviewsController,
)
from controllers.apis.interviewer.interview.request.accept import (
    InterviewerAcceptInterviewRequestController,
)

from controllers.apis.interviewer.profile.fetch import (
    InterviewerFetchProfileController,
)

from controllers.apis.location.fetch import LocationFetchAllController

from controllers.apis.message.create import MessageCreateController
from controllers.apis.message.fetch import MessageFetchAllController

from controllers.apis.skill.fetch import SkillFetchAllController

from start_utils import logger

router = APIRouter(prefix="")

# Candidate
logger.debug(f"Registering {CandidateCreateProfileController.__name__} route.")
router.add_api_route(
    path="/candidate/profile/create",
    endpoint=CandidateCreateProfileController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_CREATE_PROFILE,
)
logger.debug(f"Registered {CandidateCreateProfileController.__name__} route.")

logger.debug(
    f"Registering {CandidateAddEducationQualificationController.__name__} route."
)
router.add_api_route(
    path="/candidate/profile/education_qualification/add",
    endpoint=CandidateAddEducationQualificationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_CREATE_PROFILE,
)
logger.debug(
    f"Registered {CandidateAddEducationQualificationController.__name__} route."
)

logger.debug(
    f"Registering {CandidateAddWorkExperienceController.__name__} route."
)
router.add_api_route(
    path="/candidate/profile/work_experience/add",
    endpoint=CandidateAddWorkExperienceController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_ADD_WORK_EXPERIENCE,
)
logger.debug(
    f"Registered {CandidateAddWorkExperienceController.__name__} route."
)

logger.debug(f"Registering {CandidateAddProjectController.__name__} route.")
router.add_api_route(
    path="/candidate/profile/project/add",
    endpoint=CandidateAddProjectController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_CREATE_PROFILE,
)
logger.debug(f"Registered {CandidateAddProjectController.__name__} route.")

logger.debug(f"Registering {CandidateAddSkillController.__name__} route.")
router.add_api_route(
    path="/candidate/profile/skills/add",
    endpoint=CandidateAddSkillController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_ADD_SKILL,
)
logger.debug(f"Registered {CandidateAddSkillController.__name__} route.")

logger.debug(f"Registering {CandidateFetchProfileController.__name__} route.")
router.add_api_route(
    path="/candidate/profile/fetch",
    endpoint=CandidateFetchProfileController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_CANDIDATE_FETCH_PROFILE,
)
logger.debug(f"Registered {CandidateFetchProfileController.__name__} route.")

logger.debug(f"Registering {CandidateFetchProfilesController.__name__} route.")
router.add_api_route(
    path="/candidate/profile/fetch_all",
    endpoint=CandidateFetchProfilesController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.CANDIDATE_FETCH_PROFILES,
)
logger.debug(f"Registered {CandidateFetchProfilesController.__name__} route.")

logger.debug(f"Registering {CandidateFetchJobsController.__name__} route.")
router.add_api_route(
    path="/candidate/job/fetch_all",
    endpoint=CandidateFetchJobsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.CANDIDATE_FETCH_JOBS,
)
logger.debug(f"Registered {CandidateFetchJobsController.__name__} route.")

logger.debug(f"Registering {CandidateFetchJobController.__name__} route.")
router.add_api_route(
    path="/candidate/job/fetch",
    endpoint=CandidateFetchJobController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.CANDIDATE_FETCH_JOB,
)
logger.debug(f"Registered {CandidateFetchJobController.__name__} route.")

logger.debug(
    f"Registering {CandidateFetchJobApplicationController.__name__} route."
)
router.add_api_route(
    path="/candidate/application/fetch",
    endpoint=CandidateFetchJobApplicationController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.CANDIDATE_FETCH_APPLICATIONS,
)
logger.debug(
    f"Registered {CandidateFetchJobApplicationController.__name__} route."
)

logger.debug(
    f"Registering {CandidateFetchJobApplicationsController.__name__} route."
)
router.add_api_route(
    path="/candidate/application/fetch_all",
    endpoint=CandidateFetchJobApplicationsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.CANDIDATE_FETCH_APPLICATIONS,
)
logger.debug(
    f"Registered {CandidateFetchJobApplicationsController.__name__} route."
)

logger.debug(
    f"Registering {CandidateDeleteEducationQualificationController.__name__} route."
)
router.add_api_route(
    path="/candidate/profile/education_qualification/delete",
    endpoint=CandidateDeleteEducationQualificationController().delete,
    methods=[HTTPMethod.DELETE.value],
    name=APILK.CANDIDATE_DELETE_EDUCATION_QUALIFICATION,
)
logger.debug(
    f"Registered {CandidateDeleteEducationQualificationController.__name__} route."
)

logger.debug(f"Registering {CandidateDeleteProjectController.__name__} route.")
router.add_api_route(
    path="/candidate/profile/project/delete",
    endpoint=CandidateDeleteProjectController().delete,
    methods=[HTTPMethod.DELETE.value],
    name=APILK.CANDIDATE_DELETE_PROJECT,
)
logger.debug(f"Registered {CandidateDeleteProjectController.__name__} route.")

logger.debug(f"Registering {CandidateDeleteSkillController.__name__} route.")
router.add_api_route(
    path="/candidate/profile/skill/delete",
    endpoint=CandidateDeleteSkillController().delete,
    methods=[HTTPMethod.DELETE.value],
    name=APILK.CANDIDATE_DELETE_SKILL,
)
logger.debug(f"Registered {CandidateDeleteSkillController.__name__} route.")

logger.debug(
    f"Registering {CandidateDeleteWorkExperienceController.__name__} route."
)
router.add_api_route(
    path="/candidate/profile/work_experience/delete",
    endpoint=CandidateDeleteWorkExperienceController().delete,
    methods=[HTTPMethod.DELETE.value],
    name=APILK.CANDIDATE_DELETE_WORK_EXPERIENCE,
)
logger.debug(
    f"Registered {CandidateDeleteWorkExperienceController.__name__} route."
)

logger.debug(
    f"Registering {CandidateCreateInterviewRequestController.__name__} route."
)
router.add_api_route(
    path="/candidate/interview/request/create",
    endpoint=CandidateCreateInterviewRequestController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.CANDIDATE_CREATE_INTERVIEW_REQUEST,
)
logger.debug(
    f"Registered {CandidateCreateInterviewRequestController.__name__} route."
)

logger.debug(
    f"Registering {CandidateFetchInterviewController.__name__} route."
)
router.add_api_route(
    path="/candidate/interview/fetch",
    endpoint=CandidateFetchInterviewController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.CANDIDATE_FETCH_INTERVIEWS,
)
logger.debug(f"Registered {CandidateFetchInterviewController.__name__} route.")

logger.debug(
    f"Registering {CandidateCreateJobApplicationController.__name__} route."
)
router.add_api_route(
    path="/candidate/application/create",
    endpoint=CandidateCreateJobApplicationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYER_CREATE_JOB,
)
logger.debug(
    f"Registered {CandidateCreateJobApplicationController.__name__} route."
)

# Company
logger.debug(
    f"Registering {CompanyEmployerOnboardingEmailController.__name__} route."
)
router.add_api_route(
    path="/company/employer/onboarding/email",
    endpoint=CompanyEmployerOnboardingEmailController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.COMPANY_EMPLOYER_ONBOARDING_EMAIL,
)
logger.debug(
    f"Registered {CompanyEmployerOnboardingEmailController.__name__} route."
)

logger.debug(f"Registering {CompanyFetchCompanyController.__name__} route.")
router.add_api_route(
    path="/company/profile/fetch",
    endpoint=CompanyFetchCompanyController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_COMPANY_FETCH_PROFILE,
)
logger.debug(f"Registered {CompanyFetchCompanyController.__name__} route.")

logger.debug(f"Registering {CompanyFetchallController.__name__} route.")
router.add_api_route(
    path="/company/profile/fetch_all",
    endpoint=CompanyFetchallController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMPANY_FETCH_ALL,
)
logger.debug(f"Registered {CompanyFetchallController.__name__} route.")

logger.debug(f"Registering {CompanyFetchEmployersController.__name__} route.")
router.add_api_route(
    path="/company/employer/fetch",
    endpoint=CompanyFetchEmployersController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMPANY_FETCH_EMPLOYER_PROFILES,
)
logger.debug(f"Registered {CompanyFetchEmployersController.__name__} route.")

logger.debug(
    f"Registering {CompanyFetchCompanyJobsController.__name__} route."
)
router.add_api_route(
    path="/company/job/fetch",
    endpoint=CompanyFetchCompanyJobsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.EMPLOYEE_FETCH_COMPANY_JOBS,
)
logger.debug(f"Registered {CompanyFetchCompanyJobsController.__name__} route.")

logger.debug(
    f"Registering {CompanyFetchRecommendedApplicationsController.__name__} route."
)
router.add_api_route(
    path="/company/application/recommendations",
    endpoint=CompanyFetchRecommendedApplicationsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMPANY_FETCH_RECOMMENDATIONS,
)
logger.debug(
    f"Registered {CompanyFetchRecommendedApplicationsController.__name__} route."
)

# Currency
logger.debug(f"Registering {CurrencyFetchAllController.__name__} route.")
router.add_api_route(
    path="/{role}/currency/fetch",
    endpoint=CurrencyFetchAllController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_FETCH_CURRENCIES,
)
logger.debug(f"Registered {CurrencyFetchAllController.__name__} route.")

# Employee
logger.debug(
    f"Registering {EmployeeFetchJobApplicationsController.__name__} route."
)
router.add_api_route(
    path="/{role}/employee/application/fetch",
    endpoint=EmployeeFetchJobApplicationsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_FETCH_JOB_APPLICATIONS,
)
logger.debug(
    f"Registered {EmployeeFetchJobApplicationsController.__name__} route."
)

logger.debug(
    f"Registering {EmployeeReviewedApplicationController.__name__} route."
)
router.add_api_route(
    path="/employee/application/reviewed",
    endpoint=EmployeeReviewedApplicationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYEE_REVIEWED_JOB_APPLICATION,
)
logger.debug(
    f"Registered {EmployeeReviewedApplicationController.__name__} route."
)

logger.debug(
    f"Registering {EmployeeRecommendApplicationController.__name__} route."
)
router.add_api_route(
    path="/employee/application/recommend",
    endpoint=EmployeeRecommendApplicationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYEE_RECOMMEND_JOB_APPLICATION,
)
logger.debug(
    f"Registered {EmployeeRecommendApplicationController.__name__} route."
)

logger.debug(f"Registering {EmployeeFetchProfileController.__name__} route.")
router.add_api_route(
    path="/employee/profile/fetch",
    endpoint=EmployeeFetchProfileController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_EMPLOYEE_FETCH_PROFILE,
)
logger.debug(f"Registered {EmployeeFetchProfileController.__name__} route.")

logger.debug(
    f"Registering {EmployeeFetchCompanyJobsController.__name__} route."
)
router.add_api_route(
    path="/employee/company/job/fetch",
    endpoint=EmployeeFetchCompanyJobsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.EMPLOYEE_FETCH_COMPANY_JOBS,
)
logger.debug(
    f"Registered {EmployeeFetchCompanyJobsController.__name__} route."
)

# Employer
logger.debug(
    f"Registering {EmployerAcceptApplicationController.__name__} route."
)
router.add_api_route(
    path="/employer/application/accept",
    endpoint=EmployerAcceptApplicationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYER_ACCEPT_JOB_APPLICATION,
)
logger.debug(
    f"Registered {EmployerAcceptApplicationController.__name__} route."
)

logger.debug(f"Registering {EmployerCreateProfileController.__name__} route.")
router.add_api_route(
    path="/employer/profile/create",
    endpoint=EmployerCreateProfileController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYER_CREATE_PROFILE,
)
logger.debug(f"Registered {EmployerCreateProfileController.__name__} route.")

logger.debug(f"Registering {EmployerFetchProfileController.__name__} route.")
router.add_api_route(
    path="/employer/profile/fetch",
    endpoint=EmployerFetchProfileController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_EMPLOYER_FETCH_PROFILE,
)
logger.debug(f"Registered {EmployerFetchProfileController.__name__} route.")

logger.debug(
    f"Registering {EmployerFetchJobApplicationsController.__name__} route."
)
router.add_api_route(
    path="/{role}/employer/application/fetch",
    endpoint=EmployerFetchJobApplicationsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_FETCH_JOB_APPLICATIONS,
)
logger.debug(
    f"Registered {EmployerFetchJobApplicationsController.__name__} route."
)

logger.debug(
    f"Registering {EmployerRejectApplicationController.__name__} route."
)
router.add_api_route(
    path="/{role}/application/reject",
    endpoint=EmployerRejectApplicationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.COMMON_REJECT_JOB_APPLICATION,
)
logger.debug(
    f"Registered {EmployerRejectApplicationController.__name__} route."
)

logger.debug(
    f"Registering {EmployerUpdateApplicationProgressController.__name__} route."
)
router.add_api_route(
    path="/employer/application/update",
    endpoint=EmployerUpdateApplicationProgressController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYER_UPDATE_JOB_APPLICATION,
)
logger.debug(
    f"Registered {EmployerUpdateApplicationProgressController.__name__} route."
)

logger.debug(
    f"Registering {EmployerFetchRecommendedApplicationsController.__name__} route."
)
router.add_api_route(
    path="/employer/application/recommendations",
    endpoint=EmployerFetchRecommendedApplicationsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.EMPLOYER_FETCH_RECOMMENDATIONS,
)
logger.debug(
    f"Registered {EmployerFetchRecommendedApplicationsController.__name__} route."
)

logger.debug(
    f"Registering {EmployerHireApplicationController.__name__} route."
)
router.add_api_route(
    path="/{role}/application/hire",
    endpoint=EmployerHireApplicationController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.COMMON_HIRE_JOB_APPLICATION,
)
logger.debug(f"Registered {EmployerHireApplicationController.__name__} route.")

# Interviewer
logger.debug(
    f"Registering {InterviewerFetchInterviewRequestsController.__name__} route."
)
router.add_api_route(
    path="/interviewer/interview/request/fetch",
    endpoint=InterviewerFetchInterviewRequestsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.INTERVIEWER_FETCH_INTERVIEW_REQUESTS,
)
logger.debug(
    f"Registered {InterviewerFetchInterviewRequestsController.__name__} route."
)

logger.debug(
    f"Registering {InterviewerFetchInterviewsController.__name__} route."
)
router.add_api_route(
    path="/interviewer/interview/fetch",
    endpoint=InterviewerFetchInterviewsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.INTERVIEWER_FETCH_INTERVIEWS,
)
logger.debug(
    f"Registered {InterviewerFetchInterviewsController.__name__} route."
)

logger.debug(
    f"Registering {InterviewerAcceptInterviewRequestController.__name__} route."
)
router.add_api_route(
    path="/interviewer/interview/request/accept",
    endpoint=InterviewerAcceptInterviewRequestController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.INTERVIEWER_ACCEPT_INTERVIEW_REQUEST,
)
logger.debug(
    f"Registered {InterviewerAcceptInterviewRequestController.__name__} route."
)

logger.debug(
    f"Registering {InterviewerFetchProfileController.__name__} route."
)
router.add_api_route(
    path="/interviewer/profile/fetch",
    endpoint=InterviewerFetchProfileController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.INTERVIEWER_FETCH_PROFILE,
)
logger.debug(f"Registered {InterviewerFetchProfileController.__name__} route.")


# Job
logger.debug(f"Registering {EmployerCreateJobController.__name__} route.")
router.add_api_route(
    path="/job/create",
    endpoint=EmployerCreateJobController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.EMPLOYER_CREATE_JOB,
)
logger.debug(f"Registered {EmployerCreateJobController.__name__} route.")

logger.debug(
    f"Registering {EmployerFetchEmployerJobsController.__name__} route."
)
router.add_api_route(
    path="/employer/job/fetch",
    endpoint=EmployerFetchEmployerJobsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.EMPLOYER_FETCH_JOBS,
)
logger.debug(
    f"Registered {EmployerFetchEmployerJobsController.__name__} route."
)

logger.debug(f"Registering {EmployerDeletJobController.__name__} route.")
router.add_api_route(
    path="/employer/job/delete",
    endpoint=EmployerDeletJobController().delete,
    methods=[HTTPMethod.DELETE.value],
    name=APILK.EMPLOYER_DELETE_JOB,
)
logger.debug(f"Registered {EmployerDeletJobController.__name__} route.")

# Skill
logger.debug(f"Registering {SkillFetchAllController.__name__} route.")
router.add_api_route(
    path="/{role}/skill/fetch",
    endpoint=SkillFetchAllController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_FETCH_SKILLS,
)
logger.debug(f"Registered {SkillFetchAllController.__name__} route.")


# Location
logger.debug(f"Registering {LocationFetchAllController.__name__} route.")
router.add_api_route(
    path="/{role}/location/fetch",
    endpoint=LocationFetchAllController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_FETCH_LOCATIONS,
)
logger.debug(f"Registered {LocationFetchAllController.__name__} route.")


# CHAT
logger.debug(f"Registering {ChatCreateController.__name__} route.")
router.add_api_route(
    path="/{role}/chat/create",
    endpoint=ChatCreateController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.COMMON_CREATE_CHAT,
)
logger.debug(f"Registered {ChatCreateController.__name__} route.")


logger.debug(f"Registering {ChatFetchUserChatsController.__name__} route.")
router.add_api_route(
    path="/{role}/chat/fetch",
    endpoint=ChatFetchUserChatsController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_FETCH_CHATS,
)
logger.debug(f"Registered {ChatFetchUserChatsController.__name__} route.")

# Message
logger.debug(f"Registering {MessageCreateController.__name__} route.")
router.add_api_route(
    path="/{role}/message/create",
    endpoint=MessageCreateController().post,
    methods=[HTTPMethod.POST.value],
    name=APILK.COMMON_CREATE_MESSAGE,
)
logger.debug(f"Registered {MessageCreateController.__name__} route.")


logger.debug(f"Registering {MessageFetchAllController.__name__} route.")
router.add_api_route(
    path="/{role}/message/fetch",
    endpoint=MessageFetchAllController().get,
    methods=[HTTPMethod.GET.value],
    name=APILK.COMMON_FETCH_MESSAGES,
)
logger.debug(f"Registered {MessageFetchAllController.__name__} route.")
