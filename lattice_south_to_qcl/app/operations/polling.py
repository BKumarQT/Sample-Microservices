import requests
import aiohttp
from fastapi_utils.tasks import repeat_every
from decouple import config

from app import logger
from app.db import db

log = logger.get_logger()


async def get_order_status_equinix(s_order_id) -> dict:
    """
    Get the order status from a remote server using an asynchronous HTTP GET request.

    Parameters:
        s_order_id (str): The order ID for which to retrieve the status.

    Returns:
        str: The order status as a string.
    """
    url = f"http://35.154.194.233/get_order_status"
    params = {
        "server_id": "alpha_test",
        "south_id": "EQX",
        "order_id": s_order_id
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # Raise an exception for 4xx or 5xx HTTP status codes
                data = await response.json()
                order_status = data.get('order_status')  # Safely get the 'order_status' field
                log.info("order_Status in the ")
                return data
    except aiohttp.ClientError as e:
        # Handle any request or connection errors here
        log.error(f"An error occurred: {e}")
        return {}
    except ValueError as e:
        # Handle JSON decoding or missing 'order_status' field errors here
        log.error(f"Invalid JSON response: {e}")
        return {}


async def push_order_status(order):
    """
    Push call to QTH to update
    the order status
    :param order:
    :return:
    """
    try:
        url = config("outgoingapi url")
        response = requests.post(url=url, params=order)

        # Check the status code to see if the request was successful (200 OK)
        if response.status_code == 200:
            log.info("POST request successful! and sent order object microservice")
        # Assuming the server returns JSON data
        else:
            log.info(f"POST request failed with status code: {response.status_code}")
    except Exception as ex:
        log.error(f"Exception occurred in push order_status -> {ex}")


@repeat_every(seconds=60, raise_exceptions=True, wait_first=True)
async def get_order_status():
    """
    Polling for order status to
    the equinix via python engine
    :return:
    """
    try:
        order_objs = db["Order_details"]
        async for order in order_objs.find():
            log.info(f"Order_object from the order details document --> {order}")

            # if order.get("qcl_delete_status"):
            #    pass # remove object
            # elif order.get("qcl_order_id")
            if order.get("qcl_order_id") is None:
                log.info("order_id is None")
                pass
            else:
                order_status_obj = await get_order_status_equinix(order.get("qcl_order_id"))
                if order_status_obj.get("order_status") != order.get("qcl_order_status"):
                    await order_objs.update_one({"_id": order["_id"]},
                                                {"$set": {"qcl_order_status": order_status_obj.get("order_status")}})
                    await push_order_status(order)
                if order_status_obj["order_status"] == "CLOSED":
                    await push_order_status(order)
                    await order_objs.update_one({"_id": order["_id"]}, {"$set": {"qcl_delete_status": True}},
                                                {"$set": {"qcl_asset_id": order_status_obj.get("asset_id")}},
                                                {"$set": {"qcl_order_status": order_status_obj.get("order_status")}})
    except Exception as ex:
        log.info(f"Exception occurred get order status polling --> {ex}")
