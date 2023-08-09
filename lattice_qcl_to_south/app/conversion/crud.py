import aiohttp
import requests
from decouple import config

from app import logger

log = logger.get_logger()


class OrderOperation:
    @staticmethod
    async def push_order_id(order_obj):
        """
        This method push the order_object
        to QTH(microservice four)
        :param order_obj: dictionary
        :return: None
        """
        try:
            log.info(f"Order object to be pushed to service four -> {order_obj}")
            # Make the POST request with the given data
            url = config("qcl_update_order")
            response = requests.post(url, json=order_obj)

            # Check the status code to see if the request was successful (200 OK)
            if response.status_code == 200:
                log.info("POST request successful!")
            # Assuming the server returns JSON data
            else:
                log.info(f"POST request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            log.info(f"Error occurred: {e}")

    @staticmethod
    async def push_order_id_to_engine(order_obj):
        """
        This method is used to push the order_id
        or order object to python engine
        :param order_obj: dict
        :return: None
        """
        try:
            log.info(f"Order object to be pushed to service four -> {order_obj}")
            # Make the POST request with the given data
            url = config("python_engine_url")
            response = requests.post(url, params=order_obj)

            # Check the status code to see if the request was successful (200 OK)
            if response.status_code == 200:
                log.info("POST request successfully done to python engine")
            # Assuming the server returns JSON data
            else:
                log.info(f"POST request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            log.info(f"Error occurred: {e}")

    @staticmethod
    async def make_cross_connect_order(data, token, transaction_data):
        """
        Making a call to cross connect purchase
        order service. Using payload and auth token.
        :param transaction_data: {'transaction_id", "item_id"}
        :param data: payload for end point
        :param token: auth token
        :return: dict object
        """
        try:
            url = config("equinix_purchase_order")
            headers = {
                'authorization': f'Bearer {token}',
                'content-type': 'application/json',
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 201:
                        response_json = response.headers
                        log.info(f"Header data from the cross-connect -> {response_json}")
                        order_location = str(response_json['Location'])
                        order_id = order_location[8:]
                        order_obj = {
                            "qcl_transaction_id": transaction_data.get("qcl_transaction_id"),
                            "qcl_inventory_id": transaction_data.get("qcl_inventory_id"),
                            "order_id": order_id
                        }
                        log.info("Order successful:", response_json)
                        await OrderOperation.push_order_id(order_obj=order_obj)
                        engine_order_obj = {
                            "server_id": "alpha_test",
                            "south_id": "EQX",
                            "order_id": order_id
                        }
                        await OrderOperation.push_order_id_to_engine(engine_order_obj)

                        return response_json
                    else:
                        order_obj = {
                            "qcl_transaction_id": transaction_data.get("qcl_transaction_id"),
                            "qcl_inventory_id": transaction_data.get("qcl_inventory_id"),
                            "order_id": None
                        }
                        response_json = await response.json()
                        log.info("Failed to create order. Status code:", response.status)
                        log.info(f"Failed response from the cross connect -> {response_json}")
                        await OrderOperation.push_order_id(order_obj=order_obj)
                        return response_json
        except Exception as ex:
            log.info(f"Exception occurred while purchasing  cross connect order --> {ex}")

    # Run the asynchronous function in an event loop


order_operation_obj = OrderOperation()
