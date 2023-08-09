import json

from fastapi import (
    APIRouter,
    Depends,
    status,

)
from fastapi.requests import Request
from fastapi.responses import Response

from app import logger
from app.db import (
    get_mongo_db,
    mongo_db,
    db
)

log = logger.get_logger()

router = APIRouter(
    prefix="/internal/south-to-qcl",
    tags=["status"],
)


@router.post("/equinix/add-orders")
async def add_orders(request: Request, mongo: mongo_db = Depends(get_mongo_db)):
    """
    Add the order details object to db
    :param request: reqeust body
    :param mongo: db_session
    :return: status_code.
    """
    body_data = await request.body()
    data = json.loads(body_data)
    await mongo.add_collection(collection_name="Order_details", data=data)
    return Response(
        status_code=status.HTTP_200_OK,
        content="Successfully added the order"
    )


@router.post("/push/db")
async def push_to_db():
    obj = {
        "hello": "hi",
        "how": "are you"
    }
    await db["Order_details"].insert_one(obj)
    return Response(
        content="successfully updated",
        status_code=status.HTTP_200_OK
    )


@router.get("/get/order/details")
async def get_detatils(mongo: mongo_db = Depends(get_mongo_db)):
    order_objs = await mongo.get_collection("Order_details")
    log.info(f"Order_object from the order details document --> {order_objs}")
    async for order in order_objs.find():
        log.info(f"Order_object from the order details document --> {order}")
    return 200
