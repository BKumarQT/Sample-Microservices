from app.logger import get_logger
from app.routes import internal_api, qcl_api, db_api
from app.actions import actions

from fastapi import FastAPI

log = get_logger()

app = FastAPI(
    title="Lattice QCL Transaction Handler",
    version="0.1",
    description="Handles all the Lattice transactions",
    docs_url="/docs",
)

app.include_router(internal_api.router)
app.include_router(qcl_api.router)
app.include_router(db_api.router)


@app.get("/")
async def root():
    """_summary_

    Returns:
        _type_: _description_
    """    
    return {"message": "Welcome to QCL Transaction Handler. Please go to '/qth/api-docs' route for Swagger/OpenAPI Documentation."}

@app.get("/ping")
async def ping():
    """_summary_

    Returns:
        _type_: _description_
    """    
    return {"message": "pong"}

@app.on_event("startup")
async def startup_event():
    """_summary_
    """    
    await actions.update_tranasction_status()

