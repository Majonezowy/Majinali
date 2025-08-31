from typing import Any
import redis
from utils.logger import logger
import pickle

class nSQL:
    def __init__(self, type: str = "dict",
                       redis_host="localhost",
                       redis_port=6379,
                       redis_db=0,
                       redis_password=None) -> None:
        
        self.type = type

        if type == "dict":
            self.db = {}
        elif type == "redis":
            try:
                self.db = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    password=redis_password,
                    decode_responses=True
                )
                # Test connection
                self.db.ping()
                logger.info("✅ Connected to Redis")
            except Exception as e:
                logger.error(f"❌ Failed to connect to Redis: {e}")
                self.db = {}
                self.type = "dict"  # fallback to dict
        else:
            raise ValueError(f"Unknown NoSQL type: {type}")

    def __getitem__(self, key: Any) -> Any:
        if self.type == "redis":
            assert isinstance(self.db, redis.Redis)

            if not isinstance(key, (str, int, bytes)):
                key = pickle.dumps(key)

            value = self.db.get(key) # type: ignore
            if value is None:
                raise KeyError(key)

            try:
                return pickle.loads(value) # type: ignore
            except Exception:
                return value
        else:
            return self.db[key]
    
    def __setitem__(self, key: Any, value: Any) -> None:
        if self.type == "redis":
            assert isinstance(self.db, redis.Redis)

            if not isinstance(key, (str, int, bytes)):
                key = pickle.dumps(key)

            if not isinstance(value, (str, int, bytes)):
                value = pickle.dumps(value)

            self.db.set(key, value) # type: ignore
        else:
            self.db[key] = value

    def __contains__(self, key: Any) -> bool:
        if self.type == "redis":
            assert isinstance(self.db, redis.Redis)
            return bool(self.db.exists(key))
        return key in self.db

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __repr__(self) -> str:
        return f"<nSQL type={self.type}>"
