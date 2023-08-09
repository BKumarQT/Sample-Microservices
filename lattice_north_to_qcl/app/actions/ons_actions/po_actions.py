import requests

from app.logger import get_logger
from app.managers.document_db_manager import doc_db_manager
from app.managers.transaction_manager import transaction_manager
from app.managers.ons_manager import ons_management
from app.managers.user_manager import UserManager

# from app.db.qcl_data import convert_to_qcl

log = get_logger()


async def get_ons_data(po_id, user_manager):
    """
    Description: Functions to get ONS Details.
    Parameters : po_id
    Return: ONS details
    """
    log.info(f"Received a PO request")
    log.info(f"Get PO details")
    # get PO details
    po_details = await ons_management.get_po_details(po_id, user_manager.ons_oauth2_bearer)
    vendor_name = po_details.get("entity").get("refName")
    log.info(f"Get Items List.")
    items_list = await ons_management.ons_details(po_details['item']['links'][0]['href'], user_manager.ons_oauth2_bearer)
    log.info(f"Iterating items list")
    item_data_list = []
    for item in items_list.get("items"):
        log.info(f"Get item details")
        item_details = await ons_management.ons_details(item['links'][0]['href'], user_manager.ons_oauth2_bearer)
        inventory_item_name = item_details["item"]["refName"]
        inventory_item_id = item_details["item"]["id"]
        ons_item_data = await ons_management.ons_details(item_details["item"]['links'][0]['href'], user_manager.ons_oauth2_bearer)
        log.debug(ons_item_data)
        item_data_list.append(
            {
                "qcl_inventory_item_id" : inventory_item_id,
                "qcl_inventory_item_name" : inventory_item_name,
                "original_inventory_item_details" : ons_item_data
            }
        )
    final_data = {
        "vendor_name" : vendor_name,
        "item_details" : item_data_list
    }
    return final_data

async def convert_ons_to_qcl(ons_format_data):
    """
    Description: Functions to convert ONS to QCL.
    Parameters : ons_data
    Returns: QCL_format_data
    """
    original_inventory_item_details = ons_format_data.get("original_inventory_item_details")
    filter_query = {"type" : "crossconnect"}
    qcl_cc_data =await doc_db_manager.get_document_by_filter("ons_data", filter_query)
    qcl_crossconnect_details = {}
    for field in qcl_cc_data[0].get("details"):
        log.debug(field.get("north_value"))
        if field.get("north_value") in original_inventory_item_details:
            if field.get("type") == "dict1":
                key_name = field.get("key_name")
                if key_name not in qcl_crossconnect_details:
                    qcl_crossconnect_details[key_name] = {}
                if field.get("refName"):
                    log.debug(original_inventory_item_details.get(field.get("north_value")))
                    log.debug("-----")
                    qcl_crossconnect_details[key_name][field.get("qcl_value")] = original_inventory_item_details.get(field.get("north_value")).get("refName")
                else:
                    qcl_crossconnect_details[key_name][field.get("qcl_value")] = original_inventory_item_details.get(field.get("north_value"))
            elif field.get("type") == "str":
                if field.get("refName"):
                    qcl_crossconnect_details[field.get("qcl_value")] = original_inventory_item_details.get(field.get("north_value")).get("refName")
                else:
                    qcl_crossconnect_details[field.get("qcl_value")] = original_inventory_item_details.get(field.get("north_value"))

    qcl_format_data = {
        "qcl_inventory_item_id" : ons_format_data.get("qcl_inventory_item_id"),
        "qcl_inventory_item_name" : ons_format_data.get("qcl_inventory_item_name"),
        "qcl_crossconnect_details" : qcl_crossconnect_details
    }
    return qcl_format_data

