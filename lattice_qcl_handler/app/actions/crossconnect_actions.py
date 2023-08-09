import requests

from app.managers.transaction_manager import transaction_manager
from app.config import MS4_BASE_URL
from app.logger import get_logger

log = get_logger()

async def process_cross_connect_order(order_data):
    """_summary_

    Args:
        order_data (_type_): _description_
    """    
    lattice_transaction_id = order_data.get("lattice_transaction_id")
    for item in order_data.get("north_transaction_details_qcl_formatted"):
        qcl_inventory_item_id = item.get("qcl_inventory_item_id")
        data = {
            "lattice_transaction_id" : lattice_transaction_id,
            "qcl_inventory_item_id" : qcl_inventory_item_id,
            "qcl_cc_details" : item.get("qcl_inventory_item_details")
        }

        if send_to_south(data, order_data.get("qcl_destination_id")):
            await transaction_manager.update_transaction_item_state(lattice_transaction_id, qcl_inventory_item_id, 100)
        else:
            await transaction_manager.update_transaction_item_state(lattice_transaction_id, qcl_inventory_item_id, -100)
    await transaction_manager.update_north_update_state(lattice_transaction_id, True)         


def send_to_south(data, dest):
    """_summary_

    Args:
        data (_type_): _description_
        dest (_type_): _description_

    Returns:
        _type_: _description_
    """    
    log.debug("Sending order to MS4")
    if dest == "EQX":
        url = f"{MS4_BASE_URL}/internal/qcl-to-south/equinix/order/cc"
        log.debug(f"url: {url}")
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return True
        else:
            return False
    elif dest == "CYX":
        pass