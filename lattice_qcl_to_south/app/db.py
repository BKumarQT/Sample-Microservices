import motor.motor_asyncio
from decouple import config

from app import logger

log = logger.get_logger()

db_url = config("MONGODB_URL")

log.info(f"data base url -> {db_url}")
db_name = config("mongo_db_name")


# mongo_uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
# data = f"mongodb://{abhishek}:{hello}@localhost:27017/?authMechanism=DEFAULT
class MongoDB:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db = self.client.db_name

    async def get_collection(self, collection_name: str):
        """
        Get the given collection object
        :param collection_name: name
        :return: collection
        """
        try:
            return self.db[collection_name]
        except Exception as ex:
            log.error(f"Exception occurred while getting the collections --> {ex}")

    async def add_collection(self, collection_name: str, data):
        """
        Add the object to nosql db by providing the
        collection_name and input_data to be added.
        :param collection_name: name of the schema
        :param data: data to be inserted
        :return: None
        """
        try:
            await self.db[collection_name].insert_one(data)
        except Exception as ex:
            log.error(f"exception while adding to db --> {ex}")


mongo_db = MongoDB(config("mongo_url"))


async def get_mongo_db() -> MongoDB:
    return mongo_db
