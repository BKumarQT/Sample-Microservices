from fastapi_utils.tasks import repeat_every
import requests

from app.config import TRANSACTION_POLL_DURATION
from app.logger import get_logger
from app.managers.transaction_manager import transaction_manager
from app.config import MS2_BASE_URL

log = get_logger()

@repeat_every(seconds=TRANSACTION_POLL_DURATION)
async def update_tranasction_status():
    """
    Description: Function to iterate over transaction and retrieve and update status
    Parameters: No parameters
    """
    transactions_list = await transaction_manager.get_all_transactions()
    # log.debug(transactions_list)
    for transaction in transactions_list:
        transaction_id = transaction.get("lattice_transaction_id")
        # transaction_state = transaction.get("qcl_transaction_state")
        po_id = transaction.get("north_transaction_id")
        order_data = transaction.get("north_transaction_details_qcl_formatted")
        item_count, item_completed, item_cancelled, item_closed = 0, 0, 0, 0
        order_message = "Order Status: "
        error_message = "Error Info: "
        for order in order_data:
            item_name = order_data.get("qcl_inventory_item_name")
            item_status = order_data.get("qcl_item_status_message")
            item_err_msg = order_data.get("qcl_item_error_message")
            is_error = False
            item_count += 1
            if order.get("qcl_item_state") == 500:
                item_completed += 1
                item_closed += 1
                order_message += f"{item_name} - {item_status}, "
            elif order.get("qcl_item_state") == 600:
                item_cancelled += 1
                item_closed += 1
                order_message += f"{item_name} - {item_status}, "
            elif order.get("qcl_item_state") == 200:
                order_message += f"{item_name} - {item_status}, "
            elif order.get("qcl_item_state") < 0:
                is_error = True
                error_message += f"{item_name} - {item_err_msg}, "
                order_message += f"{item_name} - {item_status}, "

        if transaction.get("needs_north_update"):
            data = {
                "po_id" : po_id,
                "memo_message" : order_message
            }
            if is_error:
                data["vendor_message"] = error_message
            url = f"{MS2_BASE_URL}/internal/qcl_to_north/update_po_message"
            response = requests.post(url, data=data)
            if response.status_code == 200:
                await transaction_manager.update_north_update_state(transaction_id, False)
            
        if item_count == item_cancelled:
            await transaction_manager.update_transaction_status(transaction_id, 600)
            #TODO mark void
        elif item_count == item_closed:
            await transaction_manager.update_transaction_status(transaction_id, 500)
            url = f"{MS2_BASE_URL}/internal/qcl_to_north/po_complete"
            data = {"po_id" : po_id}
            response = requests.post(url, data=data)
            if response.status_code == 200:
                await transaction_manager.delete_transaction(transaction_id)
            else:
                log.error("Failed to delete PO from DB")

