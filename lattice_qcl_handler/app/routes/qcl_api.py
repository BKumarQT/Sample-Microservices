import uuid
import json

from ast import literal_eval
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request

from app import logger 
from app.managers.doc_db_manager import doc_db_manager
from app.managers.transaction_manager import transaction_manager
from app.models import QCL_Data_Object
from app.actions import crossconnect_actions


from fastapi import (
    status,
    APIRouter,
    HTTPException,
    BackgroundTasks,
)

log = logger.get_logger()

router = APIRouter(
    prefix="/qcl",
    tags=["QCL_APIs"],
)

@router.post("/accounting/crossconnect/qcl_crossconnect_order")
async def process_single_crossconnect_order(request : Request):
    """_summary_

    Args:
        qcl_data_obj (QCL_Data_Object): _description_
    """    
    # add lattice transaction id if not present
    # this would be needed for transaction coming to QTH directly.
    # qcl_data_obj = jsonable_encoder(qcl_data_obj)
    # log.debug(request.body())
    # input_data = literal_eval(request.decode('utf-8'))
    qcl_data_obj1 = await request.body()
    qcl_data_obj2 = json.loads(qcl_data_obj1)
    qcl_data_obj = json.loads(qcl_data_obj2)
    # log.debug(type(qcl_data_obj1), qcl_data_obj1)
    # log.debug(type(qcl_data_obj2), qcl_data_obj2)
    generic_data = qcl_data_obj.get("qcl_generic_data_object")
    transaction_specific_generic_data = qcl_data_obj.get("qcl_transaction_specific_data_object").get("generic_fields")
    transaction_specific_source_data = qcl_data_obj.get("qcl_transaction_specific_data_object").get("source_specific_fields")
    if generic_data.get("lattice_transaction_id") is None:    
        qcl_transaction_id = await transaction_manager.generate_lattice_transaaction_id()
    else:
        qcl_transaction_id = generic_data.get("lattice_transaction_id")
    data = {    
                "lattice_transaction_id" : qcl_transaction_id,
                "qcl_transaction_state" : 0,
                "qcl_transaction_type_name" : generic_data.get("qcl_transaction_type_name"),
                "qcl_transaction_type_number" : generic_data.get("qcl_transaction_type_number"),
                "lattice_organisation_id" : generic_data.get("lattice_organisation_id"),
                "lattice_user_id" : generic_data.get("lattice_user_id"),
                "qcl_source_id" : generic_data.get("qcl_source_id"),
                "qcl_destination_id" : generic_data.get("qcl_destination_id"),
                "north_transaction_id" : transaction_specific_source_data.get("qcl_po_id"),
                "needs_north_update" : False,
                "north_transaction_details_original" : [],
                "north_transaction_details_qcl_formatted" : []
        }

    for inventory_item in transaction_specific_source_data.get("qcl_item_details"):
        inventory_item_data = {
            "qcl_inventory_item_id" : inventory_item.get("qcl_inventory_item_id"),
            "qcl_inventory_item_name" : inventory_item.get("qcl_inventory_item_name"),
            "qcl_inventory_item_details" : inventory_item.get("qcl_crossconnect_details"),
            "qcl_item_state" : 0,
            "qcl_south_order_id" : None,
            "qcl_asset_id" : None,
            "qcl_item_status_message" : "Order received in Lattice",
            "qcl_item_error_message" : None
        }
        data["north_transaction_details_qcl_formatted"].append(inventory_item_data)

    await transaction_manager.add_new_transaction_data(data)
    log.debug("added transaction data")
    await crossconnect_actions.process_cross_connect_order(data)
    return  