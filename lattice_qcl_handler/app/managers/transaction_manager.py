import uuid

from decouple import config

from app.managers.doc_db_manager import doc_db_manager
from app.config import TRANSACTION_TABLE_NAME
from app.logger import get_logger

log = get_logger()

class Transaction_Manager:
    async def generate_lattice_transaaction_id(self):
        """_summary_

        Returns:
            _type_: _description_
        """        
        return str(uuid.uuid4())
    
    async def add_new_transaction_data(self, data):
        """_summary_

        Args:
            data (_type_): _description_
        """        
        await doc_db_manager.add_document(TRANSACTION_TABLE_NAME, data)
    
    async def update_transaction_status(self, transaction_id, transaction_state):
        """_summary_

        Args:
            transaction_id (_type_): _description_
            transaction_state (_type_): _description_
        """        
        collection_name = TRANSACTION_TABLE_NAME
        filter_query = { "lattice_transaction_id" : transaction_id}
        update_query = {"qcl_transaction_state" : transaction_state}
        await doc_db_manager.update_document(collection_name, filter_query, update_query)


    async def update_transaction_item_state(self, lattice_transaction_id, qcl_inventory_item_id, state):
        """_summary_

        Args:
            lattice_transaction_id (_type_): _description_
            qcl_inventory_item_id (_type_): _description_
            state (_type_): _description_
        """        
        
        filter_query = {
            "lattice_transaction_id" : lattice_transaction_id
        }
        trans_data = await doc_db_manager.get_document_by_filter(TRANSACTION_TABLE_NAME, filter_query)
        log.debug(trans_data)

        trans_data = await doc_db_manager.get_document_by_filter(TRANSACTION_TABLE_NAME, filter_query)
        items_data = trans_data.get("north_transaction_details_qcl_formatted")
        for i, item in enumerate(items_data):
            if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                update_query = {
                    "$set" : {
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_state" : state
                    }
                }
            await doc_db_manager.update_document(TRANSACTION_TABLE_NAME, filter_query, update_query)
            break

    async def get_all_transactions(self):
        """_summary_

        Returns:
            _type_: _description_
        """        
        return await doc_db_manager.get_all_documents(TRANSACTION_TABLE_NAME)
    
    async def update_north_update_state(self, transaction_id, state):
        """_summary_

        Args:
            transaction_id (_type_): _description_
            state (_type_): _description_
        """        
        collection_name = TRANSACTION_TABLE_NAME
        filter_query = {"lattice_transaction_id" : transaction_id}
        update_query = {
            "$set" : {
                    "needs_north_update" : state
                }
            }
        await doc_db_manager.update_document(collection_name, filter_query, update_query)
    
transaction_manager = Transaction_Manager()

