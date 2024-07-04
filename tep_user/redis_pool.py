import redis

from backend.settings import RedisDatabases, REDIS_CONNECTION_STRING

__all__ = ("RedisPoolStorage",)


class Singleton(type):
    """
    A metaclass for singleton purpose.
    Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisPoolFactory(metaclass=Singleton):
    def __init__(self):
        self._pools_register = {}

    def register_redis_pool(self, database: RedisDatabases):
        self._pools_register[database] = redis.ConnectionPool.from_url(REDIS_CONNECTION_STRING % int(database))

    def get_redis_pool(self, database: RedisDatabases) -> redis.ConnectionPool:
        if database not in self._pools_register:
            raise KeyError(f"Database {database.name} unregistered in pools register.")
        return self._pools_register[database]


RedisPoolStorage = RedisPoolFactory()

RedisPoolStorage.register_redis_pool(RedisDatabases.LOGIN_CODE)
RedisPoolStorage.register_redis_pool(RedisDatabases.IP_CONTROL)
RedisPoolStorage.register_redis_pool(RedisDatabases.LOCK)
