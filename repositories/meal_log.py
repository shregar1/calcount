from datetime import datetime
from sqlalchemy.orm import Session
from typing import List

from models.meal_log import MealLog

from abstractions.repository import IRepository
from cachetools import LRUCache, cachedmethod
from operator import attrgetter
from rapidfuzz import process, fuzz


class MealLogRepository(IRepository):

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        session: Session = None,
    ):
        super().__init__(urn, user_urn, api_name)
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._session = session
        if not self._session:
            raise RuntimeError("DB session not found")
        self._cache = LRUCache(maxsize=128)

    @property
    def urn(self):
        return self._urn

    @urn.setter
    def urn(self, value):
        self._urn = value

    @property
    def user_urn(self):
        return self._user_urn

    @user_urn.setter
    def user_urn(self, value):
        self._user_urn = value

    @property
    def api_name(self):
        return self._api_name

    @api_name.setter
    def api_name(self, value):
        self._api_name = value

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        if not isinstance(value, Session):
            raise ValueError("session must be a SQLAlchemy Session instance")
        self._session = value

    def create_record(
        self,
        meal_log: MealLog,
    ) -> MealLog:

        start_time = datetime.now()
        self._session.add(meal_log)
        self._session.commit()

        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return meal_log

    @cachedmethod(attrgetter('_cache'))
    def retrieve_record_by_urn(
        self,
        urn: str,
        is_deleted: bool = False,
    ) -> MealLog:

        start_time = datetime.now()
        record = (
            self._session.query(MealLog)
            .filter(MealLog.urn == urn, MealLog.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    @cachedmethod(attrgetter('_cache'))
    def retrieve_record_by_meal_name(
        self,
        meal_name: str,
        is_deleted: bool = False,
    ) -> MealLog:

        start_time = datetime.now()
        record = (
            self._session.query(MealLog)
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
        self,
        user_id: int,
        is_deleted: bool = False,
    ) -> List[MealLog]:

        start_time = datetime.now()
        records = (
            self._session.query(MealLog)
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
        self,
        user_id: int,
        date: datetime,
        is_deleted: bool = False,
    ) -> List[MealLog]:
        start_time = datetime.now()
        records = (
            self._session.query(MealLog)
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
            self._session.query(MealLog)
            .filter(MealLog.id == id, MealLog.is_deleted == is_deleted)
            .first()
        )
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def update_record(
        self,
        id: str,
        new_data: dict,
    ) -> MealLog:

        start_time = datetime.now()
        meal_log = (
            self._session.query(MealLog)
            .filter(MealLog.id == id)
            .first()
        )

        if not meal_log:
            raise ValueError(f"MealLog with id {id} not found")

        for attr, value in new_data.items():
            setattr(meal_log, attr, value)

        self._session.commit()
        end_time = datetime.now()
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return meal_log

    def retrieve_record_by_fuzzy_meal_name(
        self,
        meal_name: str,
        is_deleted: bool = False,
        threshold: int = 80,
    ) -> MealLog:
        """
        Retrieve the closest matching meal log by fuzzy meal name.
        """
        all_meals = (
            self._session.query(MealLog)
            .filter(MealLog.is_deleted == is_deleted)
            .all()
        )
        meal_names = [meal.meal_name for meal in all_meals]
        match, score, idx = process.extractOne(
            meal_name, meal_names, scorer=fuzz.ratio
        )
        if match and score >= threshold:
            return all_meals[idx]
        return None
