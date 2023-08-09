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

db_var = config("MONGO_URI")
db = MongoClient(db_var)

class DocumentDBManager:  # Class name should be in camel case

    def __init__(self) -> None:
        self.doc_db_client = None
        self.MONGO_URL = None
        # self.init_connection()

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
        user_details_coll = db.get_collection('USER_DETAILS')
        log.info(f"{user_details_coll}")
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

    async def add_po_state(self, lattice_id, po_id,state):
        """
        Description:  Function to add po details and state to DB.
        Parameters : lattice_id po_id, state
        Returns: Status of the insertion.
        """
        await self.init_connection()
        db = self.doc_db_client["north_to_qcl"]
        po_details_coll = db.get_collection("po_state")
        data = {"lattice_transaction_id": lattice_id,
                "po_id": po_id,
                "state": state
                }
                
        # json_data = json.dumps(data)
        po_details = po_details_coll.insert_one(data)
        await self.close_connection()
        return po_details
    
    async def add_qcl_translated_data(self, qcl_translated_data):
        """
        Description:  Function to add qcl_translated_data to DB.
        Parameters : qcl_translated_data
        Returns: Status of the insertion.
        """
        await self.init_connection()
        db = self.doc_db_client["north_to_qcl"]
        qcl_data_coll = db.get_collection("qcl_translated_data")
        qcl_details = qcl_data_coll.insert_one(qcl_translated_data)
        await self.close_connection()
        return qcl_details
    
    async def update_po_state(self, lattice_id, po_id,state):
        """
        Description:  Function to add po details and state to DB.
        Parameters : lattice_id po_id, state
        Returns: Status of the insertion.
        """
        await self.init_connection()
        db = self.doc_db_client["north_to_qcl"]
        po_details_coll = db.get_collection("po_state")
        filter_query = {"po_id": po_id}
        update_data = {
        "$set": {
        "lattice_transaction_id": lattice_id,
        "po_id": po_id,
        "state": state
                }
                }
                
        # json_data = json.dumps(data)
        result = po_details_coll.update_one(filter_query, update_data)

        await self.close_connection()
        return result

    
    
    async def get_collection_data(self, collection_name : str):
        db_name = "north_to_qcl"
        db = self.client[db_name]
        collection = db[collection_name]
        return list(collection.find())
    
    async def get_document_by_filter(self, collection_name : str, filter_query : dict):
        """
        Description: Get ONS Details from .
        Parameters : po_id
        """
        db_name = "MS1"
        await self.init_connection()
        db = self.doc_db_client[db_name]
        collection = db[collection_name]
        return list(collection.find({},{"details" : 1}))
    
    async def add_transation_data_document(self, data : dict):
        """
        Args:
            data (dict): _description_
        """        
        await self.init_connection()
        db = self.doc_db_client["MS1"]
        collection = db["ons_data"]
        collection.insert_one(data)
    
    async def get_document_by_filter_v2(self, collection_name : str, filter_query : dict):
        """
        Description: Get ONS Details from .
        Parameters : po_id
        """
        db_name = "MS1"
        await self.init_connection()
        db = self.doc_db_client[db_name]
        collection = db[collection_name]
        return list(collection.find(filter_query))


doc_db_manager = DocumentDBManager()
