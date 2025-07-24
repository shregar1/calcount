from datetime import datetime
from sqlalchemy.orm import Session
from typing import List

from models.meal_log import MealLog

from abstractions.repository import IRepository
from cachetools import LRUCache, cachedmethod
from operator import attrgetter


class MealLogRepository(IRepository):

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
        self._cache = LRUCache(maxsize=128)

    def create_record(self, meal_log: MealLog) -> MealLog:

        start_time = datetime.now()
        self.session.add(meal_log)
        self.session.commit()

        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return meal_log

    @cachedmethod(attrgetter('_cache'))
    def retrieve_record_by_urn(
        self, urn: str, is_deleted: bool = False
    ) -> MealLog:

        start_time = datetime.now()
        record = (
            self.session.query(MealLog)
            .filter(MealLog.urn == urn, MealLog.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    @cachedmethod(attrgetter('_cache'))
    def retrieve_record_by_meal_name(
        self, meal_name: str, is_deleted: bool = False
    ) -> MealLog:

        start_time = datetime.now()
        record = (
            self.session.query(MealLog)
            .filter(
                MealLog.meal_name == meal_name,
                MealLog.is_deleted == is_deleted
            )
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def retrieve_history_by_user_id(
        self, user_id: int, is_deleted: bool = False
    ) -> List[MealLog]:

        start_time = datetime.now()
        records = (
            self.session.query(MealLog)
            .filter(
                MealLog.user_id == user_id,
                MealLog.is_deleted == is_deleted
            )
            .all()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return records if records else None

    def retrieve_record_by_user_id_date(
        self, user_id: int, date: datetime, is_deleted: bool = False
    ) -> List[MealLog]:
        start_time = datetime.now()
        records = (
            self.session.query(MealLog)
            .filter(
                MealLog.user_id == user_id,
                MealLog.date == date,
                MealLog.is_deleted == is_deleted
            )
            .all()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return records if records else None

    @cachedmethod(attrgetter('_cache'))
    def retrieve_record_by_id(
        self,
        id: str,
        is_deleted: bool = False
    ) -> MealLog:
        start_time = datetime.now()
        record = (
            self.session.query(MealLog)
            .filter(MealLog.id == id, MealLog.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def update_record(self, id: str, new_data: dict) -> MealLog:

        start_time = datetime.now()
        meal_log = self.session.query(MealLog).filter(MealLog.id == id).first()

        if not meal_log:
            raise ValueError(f"MealLog with id {id} not found")

        for attr, value in new_data.items():
            setattr(meal_log, attr, value)

        self.session.commit()
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return meal_log
