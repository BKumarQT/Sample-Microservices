import requests
from app.managers.transaction_manager import transaction_manager
from app.logger import get_logger

log = get_logger()

class ONSManagement:
    def __init__(self) -> None:
        self.po_id = None
    
    async def get_po_details(self,po_id, auth):
        """
        Description:  Function to get PO Details.
        Parameters : Purchase_order_id, Bearer_token
        Returns: Returns json content containing PO details.
        """
        base_url = transaction_manager.north_details["base_url"]
        url = f"{base_url}/services/rest/record/v1/purchaseorder/{po_id}"
        log.info(f"Calling API {url}")
        response = requests.get(url, headers=auth)
        status = response.status_code
        log.info(f"Response status code: {status}")
        return response.json()
    
    async def ons_details(self,url, auth):
        """
        Description:  Function to get ONS Details.
        Parameters : ONS URL, Bearer_token
        Returns: Returns json content containing ONS details.
        """
        log.info(f"Calling API {url}")
        response = requests.get(url, headers=auth)
        status = response.status_code
        log.info(f"Response status code: {status}")
        return response.json()
    
    async def get_ons_item_details(self,item_details, user_mngr):
        """
        Description:  Function to get ONS Details.
        Parameters : ONS URL, Bearer_token
        Returns: Returns json content containing ONS details.
        """
        item_name = item_details['item']['refName']
        log.info(f"Found item {item_name}")
        log.info(f"Get {item_name} details")
        item_data = await ons_management.ons_details(item_details['item']['links'][0]['href'], user_mngr.ons_oauth2_bearer)
        return f"Successfully fetched Item details.", item_data
    
    async def call_qth(self,qcl_data):
        """
        Description:  Function to QCL Transaction handler.
        Parameters : QCL Data
        Returns: Returns status code of the call.
        """
        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://localhost:8003/accounting/crossconnect/qcl_crossconnect_order_single"
        requests.post(url, headers=headers, data=qcl_data)

ons_management = ONSManagement()


