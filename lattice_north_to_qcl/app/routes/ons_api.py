from datetime import datetime
from bson import ObjectId
import json

from fastapi import (
    APIRouter,
    BackgroundTasks
)

from app import logger
from app.actions.ons_actions import po_actions
from app.managers.document_db_manager import doc_db_manager
from app.managers.transaction_manager import transaction_manager
from app.managers.user_manager import UserManager
from app.managers.ons_manager import ons_management

router = APIRouter(
    prefix="/ons",
    tags=["ONS_APIs"],
)

log = logger.get_logger()

# Custom JSON serialization function
def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

async def process_po(po_data: dict,lattice_transaction_id):
    """
    Description: API to process purchase order
    Parameters: po_data
    Returns: Qcl translated data
    """
    po_id = po_data.get("podetails").get("id")
    user_manager = UserManager("qarbon_user")
    ons_po_details = await po_actions.get_ons_data(po_id, user_manager)
    if "equinix" in ons_po_details.get("vendor_name").lower():
        destination_id = "EQX"
    elif "cyxtera" in ons_po_details.get("vendor_name").lower():
        destination_id = "CYX"

    # convert item data to qcl format
    qcl_converted_items = []
    for item in ons_po_details.get("item_details"):
        qcl_converted_items.append(await po_actions.convert_ons_to_qcl(item))

    # create generic data object    
    generic_obj_data = {
        "lattice_transaction_id" : lattice_transaction_id,
        "lattice_organisation_id" : user_manager.organisation_id,
        "lattice_user_id" : user_manager.user_id,
        "qcl_category" : "accounting",
        "qcl_sub_category" : "crossconnect",
        "qcl_transaction_data" : {
                                    "qcl_transaction_type_number" : "003010001012",
                                    "qcl_transaction_type_name" : "QCL_ORDER_CC"
                                },
        "qcl_source_id" : "ONS",
        "qcl_destination_id" : destination_id
    }

    # create transaction specific object
    transaction_specific_obj_data = {
        "generic_fields" : {
                            "time_initiated" : str(datetime.now())
                        },
        "source_specific_fields" : {
                            "qcl_po_id" : po_id,
                            "qcl_item_details" : qcl_converted_items,
                            "original_item_details" : ons_po_details.get("item_details")
                        },
        "destination_specific_fields": {}
    }


    qcl_data_object = {
        "qcl_generic_data_object" : generic_obj_data,
        "qcl_transaction_specific_data_object" : transaction_specific_obj_data
    }
    await doc_db_manager.add_qcl_translated_data(qcl_data_object)
    

    log.debug(qcl_data_object)
    qcl_data_object = json.dumps(qcl_data_object, default=json_serial)
    await ons_management.call_qth(qcl_data_object)
    await doc_db_manager.update_po_state(lattice_transaction_id,po_id,1)




@router.post("/process_po")
async def send_notification(po_data:dict, background_tasks: BackgroundTasks):
    """
    Description: API to send sucessful response after fetching data in Lattice
    Parameters: po_data
    Returns: Sucessful response 
    """
    lattice_transaction_id = await transaction_manager.generate_lattice_transaaction_id()
    po_id = po_data.get("podetails").get("id")
    await doc_db_manager.add_po_state(lattice_transaction_id,po_id,0)
    background_tasks.add_task(process_po, po_data,lattice_transaction_id)
    return {"message": "Sucessfully fetched data"}


    