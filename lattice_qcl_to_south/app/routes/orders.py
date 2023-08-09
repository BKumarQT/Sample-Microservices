import json

import aiohttp
from decouple import config
from fastapi import (
    status,
    APIRouter,
    HTTPException,
    BackgroundTasks,
    Depends,
)
from fastapi.requests import Request
from fastapi.responses import Response

from app import logger
from app.conversion.crud import order_operation_obj
from app.conversion.data_map import map_obj
from app.db import (
    mongo_db,
    get_mongo_db,
)

log = logger.get_logger()

router = APIRouter(
    prefix="/internal/qcl-to-south",
    tags=["order"],
)

client_id = config('EQX_CLIENT_ID')
client_secret = config('EQX_CLIENT_SECRET')


async def get_access_token() -> str:
    """
    Get the access token from the
    EQX service by providing client_id
    and secret_id.
    :return: access_token
    """
    log.info(f"EQx-Client-id and EQX-Secret-id while generating token respectively --> {client_id}  {client_secret}")
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(config("token_url"), data=payload) as response:
            json_response = await response.json()
            access_token = json_response.get("access_token")
            log.info(f"access_token for creating purchase order -> {access_token}")
            return access_token


@router.post("/equinix/order/cc")
async def order_create(
        request: Request,
        bg_task: BackgroundTasks,
        mongo: mongo_db = Depends(get_mongo_db)
):
    """
    Create the purchase order using request
    body data.
    :param mongo: mongo_db_connection
    :param bg_task: runs and execute in background_thread
    :param request: request_body
    :return: response object status_code->201
    """
    try:
        body = await request.body()

        # await db["qcl_transaction"].insert_one(body)  # without using dependency
        payload = await map_obj.qcl_to_equinox(json.loads(body))
        token = await get_access_token()

        order_id = await order_operation_obj.make_cross_connect_order(payload, token, json.loads(body))
        transaction_details = {
            "before_translation_to_equinix": json.loads(body),
            "after_translation_to_equinix": payload,
            "order_id": str(order_id)
        }
        await mongo.add_collection(collection_name="transaction_details", data=transaction_details)  # debug mode
        # bg_task.add_task(order_operation_obj.make_cross_connect_order, payload, token)
        log.info(f"request body from the QCL service --> {body} and type of body {type(body)}")
        log.info(f"Order id from the cross connect -> {order_id}")
        return Response(
            status_code=status.HTTP_201_CREATED,
            content="Successfully created order"
        )
    except Exception as ex:
        raise HTTPException(
            detail=f"Exception while purchasing the order -> {ex}",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/push/db")
async def push_to_db(mongo: mongo_db = Depends(get_mongo_db)):
    log.info(f"mongo db_object---> {mongo}")
    collection = await mongo.get_collection(collection_name="transaction")
    # await mongo.add_collection(collection_name="transaction", data={"hi": "hello"})
    log.info(f"collection_data --> {collection}")
    return 200
