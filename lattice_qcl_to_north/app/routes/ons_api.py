import requests

from datetime import datetime


from fastapi import (
    APIRouter,
)

from app.logger import get_logger
from app.actions.ons_actions.po_actions import update_po_status
from app.managers.transaction_manager import transaction_manager
from app.managers.user_manager import UserManager
from app.managers.ons_manager import ons_management

router = APIRouter(
    prefix="/ons",
    tags=["ONS_APIs"],
)

log = get_logger()


@router.patch("/update_po_message")
async def update_po(message_dict:dict):
    """
    Description: Function to update po with status of the order
    Parameters: po_id, memo_message,vendor_message
    Returns: Updates PO with desired message
    """
    user_manager = UserManager("qarbon_user")
    log.info("Checking for the message")
    if "message" in message_dict:
        message=message_dict["message"]
        if "memo_message" in message.keys() and "vendor_message" in message.keys():
            update_type="vendor"
            status = await update_po_status(update_type,message,message_dict["po_id"],user_manager,message_dict["t_id"])

        elif "memo_message" in message.keys():
            update_type = "memo"
            status = await update_po_status(update_type,message,message_dict["po_id"],user_manager,message_dict["t_id"])
        return status

@router.post("/mark_po_complete")
async def mark_item_received(po_id,t_id):
    """
    Description: Function to mark po status to pending bill
    Parameters: po_id, t_id
    Returns: Marks it to pending bill
    """
    BASE_URL = transaction_manager.north_details["base_url"]
    url = f"{BASE_URL}/services/rest/record/v1/purchaseOrder/{po_id}/!transform/itemReceipt"
    log.poc_log(f"[{t_id}] Updating PO status to 'PENDING BILL'.")
    log.poc_log(f"[{t_id}] Calling API : {url}")
    response = requests.post(url, headers=UserManager.get_oauth2_bearer())
    status_code = response.status_code
    log.poc_log(f"[{t_id}] API response status code: {status_code}")
    return f"{status_code} Sucessfully marked ONS received."


