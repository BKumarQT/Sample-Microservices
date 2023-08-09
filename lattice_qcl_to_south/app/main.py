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
from app.routes import orders

log = logger.get_logger()

app = FastAPI(
    title="Lattice Q-C-L to south",
    version="0.1",
    description="Q-C-L to South order purchase",
)


@app.get("/")
async def welcome():
    return "Welcome to South order purchase service"


@app.get("/ping")
async def ping():
    """
    Test/Check Redis connection
    :return: str
    """
    await redis_obj.set_key("hello", "welcome to redis")
    return await redis_obj.get_key("hello")


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


app.include_router(orders.router)
