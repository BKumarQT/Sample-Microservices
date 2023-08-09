from fastapi import FastAPI
import requests

from app.config import INSTRUCTIONS_PATH
from app.logger import get_logger
from app.process_instructions import process_file
from app.routes import ons_api
from app.managers.document_db_manager import doc_db_manager, db

log = get_logger()

app = FastAPI(title="Lattice North to QCL",
              version="0.1",
              description="Interface for north incoming transactions and North to QCL conversion",
              docs_url="/docs")

app.include_router(ons_api.router)


@app.on_event("startup")
async def startup_event():
    # inital update to document db
    # comment the function if data is already added to DB
    # await init_populate_doc_db()
    log.info("Starting instructions processor.")
    await process_file(INSTRUCTIONS_PATH)


@app.get("/")
async def root():
    return {
        "message": "Welcome to North to QCL Microservice. Please go to '/north_to_qcl/api-docs' route for "
                   "Swagger/OpenAPI Documentation."
    }


@app.get("/ping")
async def ping():
    """
    Description: API to ping the server to check if it's running.
    Parameters : No parameters
    Returns: A dictionary containing a 'message' key with the value 'pong'.
    """
    return {"message": "pong"}

@app.post("/add_translation_data")
async def add_translation_data(data : dict):
    """
    Args:
        data (dict): _description_
    """
    await doc_db_manager.add_transation_data_document(data)

@app.get("/connect_ms3")
async def ping_ms3():
    status = requests.get("http://192.168.68.104:8003/ping")
    print(status)
    return status.status_code

# @router.post("/push/db")
# async def push_to_db(mongo: mongo_db = Depends(get_mongo_db)):
#     log.info(f"mongo db_object---> {mongo}")
#     collection = await mongo.get_collection(collection_name="transaction")
#     # await mongo.add_collection(collection_name="transaction", data={"hi": "hello"})
#     log.info(f"collection_data --> {collection}")
#     return 200