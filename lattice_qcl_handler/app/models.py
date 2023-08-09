from pydantic import BaseModel
from typing import Optional


class QCL_Data_Object(BaseModel):
    qcl_generic_data_object: dict
    qcl_transaction_specific_data_object: dict

class Order_Details(BaseModel):
    lattice_transaction_id: str
    qcl_inventory_item_id : str
    qcl_order_status : Optional[str] = None
    qcl_asset_id : Optional[str] = None
    qcl_destination_id : Optional[str] = None
    qcl_order_id : str

