from datetime import datetime
from sqlalchemy.orm import Session

from models.profile import Profile

from abstractions.repository import IRepository


class ProfileRepository(IRepository):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        session: Session = None,
    ):
        super().__init__(urn, user_urn, api_name)
        self.urn = urn
        self.user_urn = user_urn
        self.api_name = api_name
        self.session = session

        if not self.session:
            raise RuntimeError("DB session not found")

    def create_record(self, profile: Profile) -> Profile:

        start_time = datetime.now()
        self.session.add(profile)
        self.session.commit()

        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return profile

    def retrieve_record_by_urn(
        self, urn: str, is_deleted: bool = False
    ) -> Profile:

        start_time = datetime.now()
        record = (
            self.session.query(Profile)
            .filter(Profile.urn == urn, Profile.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def retrieve_record_by_user_id(
        self, user_id: int, is_deleted: bool = False
    ) -> Profile:

        start_time = datetime.now()
        record = (
            self.session.query(Profile)
            .filter(
                Profile.user_id == user_id,
                Profile.is_deleted == is_deleted,
            )
            .one_or_none()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record

    def update_record(self, id: str, new_data: dict) -> Profile:

        start_time = datetime.now()
        profile = self.session.query(Profile).filter(Profile.id == id).first()

        if not profile:
            raise ValueError(f"Profile with id {id} not found")

        for attr, value in new_data.items():
            setattr(profile, attr, value)

        self.session.commit()
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return profile
