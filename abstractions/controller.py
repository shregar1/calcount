from abc import ABC
from datetime import datetime
from http import HTTPStatus

from errors.bad_input_error import BadInputError

from models.api_lk import APILK
from models.transaction_log import TransactionLog

from repositories.api_lk import APILKRepository
from repositories.transaction_log import TransactionLogRepository

from start_utils import db_session, logger

from utilities.dictionary import DictionaryUtility


class IController(ABC):

    def __init__(
        self, urn: str = None, user_urn: str = None, api_name: str = None
    ) -> None:
        super().__init__()
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.logger = logger.bind(urn=self.urn)
        self.dictionary_utility = DictionaryUtility(urn=self.urn)

    async def create_transaction_log(
        self,
        urn: str,
        user_id: int,
        reference_urn: str,
        request_timestamp: datetime,
        request_payload: dict,
        request_headers: dict,
        created_at: datetime,
        created_by: int,
    ) -> None:

        try:

            self.transaction_log_repository = TransactionLogRepository(
                urn=self.urn,
                user_urn=self.user_urn,
                api_name=self.api_name,
                session=db_session,
            )

            self.logger.debug("Validating duplicate reference urn")
            records = self.transaction_log_repository.retrieve_record_by_reference_urn_user_id(
                reference_urn=reference_urn, user_id=user_id
            )

            self.logger.debug("Preparing new transaction log")
            transaction_log: TransactionLog = TransactionLog(
                urn=urn,
                api_id=None,
                user_id=user_id,
                reference_number=reference_urn,
                request_payload=request_payload,
                request_headers=request_headers,
                request_timestamp=request_timestamp,
                created_on=created_at,
                created_by=created_by,
            )

            self.transaction_log: TransactionLog = (
                self.transaction_log_repository.create_record(
                    transaction_log=transaction_log
                )
            )

            self.logger.debug("Prepared new transaction log")

        except Exception as err:
            self.logger.error(err)
            db_session.rollback()

        if records:
            raise BadInputError(
                responseMessage="Duplicate reference urn",
                responseKey="error_duplicate_reference_urn",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )
        self.logger.debug("Verified duplicate reference urn")

        return None

    async def update_transaction_log(
        self,
        urn: str,
        user_id: int,
        api_id: int,
        response_timestamp: datetime,
        response_payload: dict,
        response_headers: dict,
        http_status_code: int,
        response_key: str,
    ) -> None:

        self.transaction_log_repository = TransactionLogRepository(
            urn=self.urn,
            user_urn=self.user_urn,
            api_name=self.api_name,
            session=db_session,
        )

        self.logger.debug("Updating transaction log")
        transaction_log: TransactionLog = (
            self.transaction_log_repository.retrieve_record_by_urn(urn=urn)
        )

        response_payload["data"] = self.dictionary_utility.mask_dict_values(
            response_payload.get("data", {})
        )

        transaction_log.api_id = api_id
        transaction_log.response_timestamp = response_timestamp
        transaction_log.request_payload = response_payload
        transaction_log.response_headers = response_headers
        transaction_log.response_key = response_key
        transaction_log.http_status_code = http_status_code
        transaction_log.updated_on = datetime.now()
        transaction_log.updated_by = user_id

        db_session.commit()
        self.logger.debug("Updated transaction log")

        return None

    async def validate_request(
        self,
        urn: str,
        user_urn: str,
        request_payload: dict,
        request_headers: dict,
        api_name: str,
        user_id: str,
    ):

        self.user_urn = user_urn
        self.api_name = api_name
        self.api: APILK = None

        self.api_lk_repository = APILKRepository(
            urn=self.urn,
            user_urn=self.user_urn,
            api_name=self.api_name,
            session=db_session,
        )

        self.api: APILK = self.api_lk_repository.retrieve_record_by_name(
            self.api_name
        )
        if self.api is None:
            raise BadInputError(
                responseMessage="Invalid API",
                responseKey="error_invalid_api",
                http_status_code=HTTPStatus.BAD_REQUEST,
            )

        return
