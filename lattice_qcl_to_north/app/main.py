from fastapi import FastAPI

from app.config import INSTRUCTIONS_PATH
from app.logger import get_logger
from app.process_instructions import process_file
from app.routes import ons_api

log = get_logger()

app = FastAPI(title="Lattice QCL to North",
              version="0.1",
              description="Interface for QCL outgoing transactions to North ")




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
        "message": "Welcome to North to QCL Microservice. Please go to '/qcl_to_north/api-docs' route for "
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


app.include_router(ons_api.router)