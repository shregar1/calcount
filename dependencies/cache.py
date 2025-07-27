from redis import Redis

from start_utils import redis_session


class CacheDependency:

    @staticmethod
    def derive() -> Redis:
        return redis_session
