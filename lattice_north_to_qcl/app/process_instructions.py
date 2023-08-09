from app.logger import get_logger
from app.managers.transaction_manager import transaction_manager
# from app.managers.redis_manager import redis_manager
import yaml

log = get_logger()


async def process_file(file_path):
    """
    This parses through the instructions file and executes the instructions.
    """
    log.info("Reading instructions file.")
    with open(file_path, "r") as ins:
        instructions_data = yaml.safe_load(ins)

    for key in instructions_data.keys():
        # store north and south data
        if key == "INIT":
            log.info("Found instruction INIT")
            log.info("Loading north and south details")
            transaction_manager.north_details = instructions_data[key]["north_details"]
            log.info("Successfully loaded north details")

        # initialise redis
        elif key == "REDIS":
            log.info("Found instruction REDIS")
            log.info("Setting up redis")
            # await redis_manager.init_redis(instructions_data[key])

        # # polling north for PO
        # elif key == "POLL_PurchaseOrder":
        #     log.info("Found instruction POLL_PurchaseOrder")
        #     # instructions_manager.PO_POLL_DATA = instructions_data[key]
        #     await actions.Poll_PurchaseOrder()
