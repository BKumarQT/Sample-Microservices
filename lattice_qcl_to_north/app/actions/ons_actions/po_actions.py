import requests

from app.logger import get_logger
from app.managers.document_db_manager import doc_db_manager
from app.managers.transaction_manager import transaction_manager
from app.managers.ons_manager import ons_management
from app.managers.user_manager import UserManager

# from app.db.qcl_data import convert_to_qcl

log = get_logger()




async def update_po_status(type,message,po_id, user_manager, t_id):
    """
    Description: Function to update po status 
    Parameters: po_id, t_id,update_message
    Returns: Updates to desired message
    """
    if type=="memo":
        data = {
                    "memo" : message["memo_message"]
                }
        BASE_URL = transaction_manager.north_details["base_url"]
        po_url = f"{BASE_URL}/services/rest/record/v1/purchaseorder/{po_id}"
        log.info(f"[{t_id}] Calling API : {po_url}")
        response = requests.patch(po_url, json=data, headers=user_manager.ons_oauth2_bearer)
        if response.status_code == 204:
            return (f"[{t_id}] Successfully updated status in ONS")
        else:
            return (f"[{t_id}] Failed to update status in ONS. Status code: {response.status_code}")
    elif type=="vendor":
            data = {
                "memo": message["memo_message"],
                "message" : message["vendor_message"]
            }
            BASE_URL = transaction_manager.north_details["base_url"]
            po_url = f"{BASE_URL}/services/rest/record/v1/purchaseorder/{po_id}"
            response = requests.patch(po_url, json=data, headers=user_manager.ons_oauth2_bearer)

            if response.status_code == 204:
                return (f"[{t_id}] Successfully updated vendor message in ONS")
                # log.poc_log(f"[{transaction_manager.transaction_id}] API response status code: 204")
            else:
                return (f"[{t_id}] Failed to update vendor message in ONS. Status code: {response.status_code} {response.content}")

