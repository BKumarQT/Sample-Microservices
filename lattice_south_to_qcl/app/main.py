from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Depends,
)

from app import logger
from app.db import (
    get_mongo_db,
    mongo_db,
)
from app.redis import redis_obj
from app.routes import south_status
from app.operations.polling import get_order_status

log = logger.get_logger()

app = FastAPI(
    title="South to QCL",
    version="0.1",
    description="South order status",
)


@app.get("/")
async def welcome():
    return "Welcome to South order status"


@app.get("/ping")
async def ping():
    """
    Test/Check Redis connection
    :return: str
    """
    await redis_obj.set_key("ping", "pong")
    return await redis_obj.get_key("ping")


@app.on_event("startup")
async def on_startup():
    log.debug("Startup Server")
    try:
        pass
        await get_order_status()
    except Exception as ex:
        log.info(f"Error occurred in startup event -> {ex}")


@app.on_event("shutdown")
async def on_shutdown():
    log.debug("shutdown")


@app.get("/test/db")
async def test_connection(mongo: mongo_db = Depends(get_mongo_db)):
    """
    Check db connection.
    :return: status_code
    """
    try:
        log.info(f"mongo database object --> {mongo}")
        return 200
    except Exception as ex:
        log.info(f"exception occurred while testing the db connection -> {ex}")
        raise HTTPException(
            detail=f"Unable to connect db  -> {ex}",
            status_code=status.HTTP_404_NOT_FOUND,
        )


app.include_router(south_status.router)
