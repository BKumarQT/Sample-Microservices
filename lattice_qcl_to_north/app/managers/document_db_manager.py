from decouple import config
from pymongo import MongoClient

from app.constants import (
    DOC_DB_NAME,
    USER_COLLECTION_NAME,
    NORTH_COLLECTION_NAME,
    NORTH_DETAILS,
)
from app.logger import get_logger

log = get_logger()


class DocumentDBManager:  # Class name should be in camel case

    def __init__(self) -> None:
        self.doc_db_client = None
        self.MONGO_URL = None

    async def init_connection(self):
        """
        Description:  Function to initialise DB Connection.
        Parameters : 
        Returns: Status of the connection.
        """
        if config("environment") == "DEV":
            self.MONGO_URL = config("MONGO_URI")
        elif config("environment") == "PROD":
            self.MONGO_URL = config("MONGO_URI")

        try:
            self.doc_db_client = MongoClient(self.MONGO_URL)
            log.info("Connected to db")
        except Exception as e:
            log.error(f"Failed to connect to DB. {e}")

    async def close_connection(self):
        """
        Description:  Function to close DB Connection.
        Parameters : 
        Returns: Status of the connection.
        """
        self.doc_db_client.close()

    async def get_user_details(self, organisation):
        """
        Description:  Function to get user details.
        Parameters : 
        Returns: Returns user data.
        """
        log.info("Retreiving user info from db")
        await self.init_connection()
        db = self.doc_db_client[DOC_DB_NAME]
        user_details_coll = db.get_collection(USER_COLLECTION_NAME)
        user_data = list(user_details_coll.find({"organization": organisation}, {'_id': False}))
        await self.close_connection()
        log.info("successfully fetched user data from db")
        return user_data

    async def get_north_API_details(self, north_id):  # method name should be in lower case
        """
        Description:  Function to get North API details.
        Parameters : 
        Returns: Returns North data.
        """
        await self.init_connection()
        db = self.doc_db_client[DOC_DB_NAME]
        north_details_coll = db.get_collection(NORTH_COLLECTION_NAME)
        north_data = north_details_coll.find_one({"north_id": north_id}, {'_id': False})
        await self.close_connection()
        return north_data

    async def add_ons_details(self, organisation, po_id, item_details):
        """
        Description:  Function to add ons details to DB.
        Parameters : organisation, po_id, item_details
        Returns: Status of the insertion.
        """
        await self.init_connection()
        db = self.doc_db_client[DOC_DB_NAME]
        po_details_coll = db.get_collection(NORTH_DETAILS)
        data = {"organization": organisation,
                "po_id": {po_id: {
                    "item_details": item_details
                }
                }}
        # json_data = json.dumps(data)
        po_details = po_details_coll.insert_one(data)
        await self.close_connection()
        return po_details
    
    async def get_collection_data(self, collection_name : str):
        db_name = "north_to_qcl"
        db = self.client[db_name]
        collection = db[collection_name]
        return list(collection.find())
    
    async def get_document_by_filter(self, collection_name : str, filter_query : dict):
        db_name = "MS1"
        await self.init_connection()
        db = self.doc_db_client[db_name]
        collection = db[collection_name]
        return list(collection.find({},{"details" : 1}))


doc_db_manager = DocumentDBManager()
