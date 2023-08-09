import json

from rediscluster import RedisCluster
import redis
from decouple import config

from app.managers.document_db_manager import doc_db_manager
from app.logger import get_logger

log = get_logger()


class RedisManager:
    def __init__(self) -> None:
        # create connection to redis instance
        self.north_list = None
        self.organisation = None
        if config("environment") == "PROD":
            self.host = config("REDIS_HOST")
            self.port = config("REDIS_PORT")
            startup_nodes = [{"host": self.host, "port": self.port}]
            self.redis = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True,
                                      ssl=True)
        elif config("environment") == "DEV":
            self.redis = redis.Redis()

        # verify connection
        # if self.redis.ping():
        #     log.info("Initialized redis connection")
        # else:
        #     log.error("Failed to initialize redis")

    async def init_redis(self, redis_data):
        """
        This function fetches the necessary data from the master DB and populates into redis.
        """
        self.organisation = redis_data["ORGANISATION"]
        self.north_list = redis_data["NORTH"]

        # update redis data
        log.info(f"Fetching user details for {self.organisation} organisation")
        await self.update_user_details()
        log.info(f"Fetching API details for {self.north_list}")
        await self.update_north_api_details()

        # initialise PO details dict
        
    async def update_user_details(self):
        """
        This function fetches user details from master DB and loads to redis.
        """
        user_data = await doc_db_manager.get_user_details(self.organisation)
        self.redis.set('user_data', json.dumps(user_data))
        log.info("Loaded user details to redis")

    async def update_north_api_details(self):
        """
        This function fetches API details of north side from master DB and loads to redis.
        """
        north_data = {}
        for north in self.north_list:
            north_api_data = await doc_db_manager.get_north_API_details(north)
            north_data[north] = north_api_data
        self.redis.set('north_data', json.dumps(north_data))
        log.info("Loaded north API details to redis")


# redis_manager = RedisManager()
