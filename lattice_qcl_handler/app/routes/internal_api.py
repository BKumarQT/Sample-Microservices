import json 

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request


from app import logger 
from app.managers.transaction_manager import transaction_manager
from app.managers.doc_db_manager import doc_db_manager
from app.config import TRANSACTION_TABLE_NAME
from app.models import Order_Details

log = logger.get_logger()

router = APIRouter(
    prefix="/internal",
    tags=["INTERNAL_APIs"],
)

@router.post("/qth/update_equinix_order")
async def update_equinix_order(request : Request):
    """_summary_

    Args:
        order_details (Order_Details): _description_
    """
    order_details1 = await request.body()
    order_details2 = json.loads(order_details1)
    order_details = json.loads(order_details2)
    log.debug(order_details)
    # order_details = jsonable_encoder(order_details)
    log.debug("Request Data --->", order_details)
    lattice_transaction_id = order_details.get("lattice_transaction_id")
    qcl_inventory_item_id = order_details.get("qcl_inventory_item_id")
    order_id = order_details.get("qcl_order_id")
    filter_query = {
                "lattice_transaction_id" : lattice_transaction_id
            }
    trans_data = await doc_db_manager.get_document_by_filter(TRANSACTION_TABLE_NAME, filter_query)
    items_data = trans_data.get("north_transaction_details_qcl_formatted")
    if order_id == "":
        for i, item in enumerate(items_data):
            error_message = order_details.get("qcl_error_message")
            if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                update_query = {
                    "$set" : {
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_error_message" : error_message,
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_state" : -200
                    }
                }
                await doc_db_manager.update_document(TRANSACTION_TABLE_NAME, filter_query, update_query)
                await transaction_manager.update_north_update_state(lattice_transaction_id, True)
                break
    else: 
        for i, item in enumerate(items_data):
            if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                update_query = {
                    "$set" : {
                        f"north_transaction_details_qcl_formatted.{i}.qcl_south_order_id" : order_id,
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_state" : 200
                    }
                }
                await doc_db_manager.update_document(TRANSACTION_TABLE_NAME, filter_query, update_query)
                await transaction_manager.update_north_update_state(lattice_transaction_id, True)
                break

@router.post("/qth/order_status_updated")
async def update_item_order_status(order_details : Order_Details):
    """_summary_

    Args:
        order_details (Order_Details): _description_
    """
    order_details = jsonable_encoder(order_details)
    lattice_transaction_id = order_details.get("lattice_transaction_id")
    qcl_inventory_item_id = order_details.get("qcl_inventory_item_id")
    qcl_order_status = order_details.get("qcl_order_status")
    filter_query = {
            "lattice_transaction_id" : lattice_transaction_id
        }
    log.debug(type(lattice_transaction_id))
    trans_data = await doc_db_manager.get_document_by_filter(TRANSACTION_TABLE_NAME, filter_query)
    log.debug(trans_data)
    items_data = trans_data.get("north_transaction_details_qcl_formatted")
    item_found = False
    for i, item in enumerate(items_data):
        if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
            item_found = True
            break
    if not item_found:
        log.error(f"Item not found in transaction")
        return
    
    if order_details.get("qcl_destination_id") == "EQX":
        if order_details.get("qcl_order_status") == "CLOSED":
            update_query = {
                "$set" : {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message" : qcl_order_status,
                    f"north_transaction_details_qcl_formatted.{i}.qcl_asset_id" : order_details.get("qcl_asset_id")
                }
            }
            doc_db_manager.update_document(TRANSACTION_TABLE_NAME, filter_query, update_query)
            transaction_manager.update_transaction_item_state(lattice_transaction_id, qcl_inventory_item_id, 500)
        else:
            update_query = {
                "$set" : {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message" : qcl_order_status,
                }
            }
            doc_db_manager.update_document(TRANSACTION_TABLE_NAME, filter_query, update_query)
            if order_details.get("qcl_order_status") == "CANCELLED":
                transaction_manager.update_transaction_item_state(lattice_transaction_id, qcl_inventory_item_id, 600)
        await doc_db_manager.update_document(TRANSACTION_TABLE_NAME, filter_query, update_query)

    await transaction_manager.update_north_update_state(lattice_transaction_id, True)