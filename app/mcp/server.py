from fastapi import FastAPI, Header, HTTPException
from app.mcp.reservation_writer import ReservationWriter
from app.utils.logger import logger
from app.utils.config import FASTAPI_MCP_URL, FASTAPI_MCP_API_KEY   


app = FastAPI(title="SmartPark MCP Server")

writer = ReservationWriter()
API_URL = FASTAPI_MCP_URL
API_KEY = FASTAPI_MCP_API_KEY




# ----------------------------------------------------
# API Key Validation
# ----------------------------------------------------

def validate(api_key: str):

    if api_key != API_KEY:

        logger.warning("MCP Server | Unauthorized API access attempted")

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )


# ----------------------------------------------------
# Sync Approved Reservations
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "SmartPark MCP Server Running"
    }

@app.post("/sync-approved")
def sync_approved(x_api_key: str = Header(...)):

    validate(x_api_key)

    writer.write_approved_reservations()

    

    return {
        "status": "success",
        "message": "Approved reservations synchronized."
    }


# ----------------------------------------------------
# Sync Rejected Reservations
# ----------------------------------------------------

@app.post("/sync-rejected")
def sync_rejected(x_api_key: str = Header(...)):

    validate(x_api_key)

    writer.write_rejected_reservations()

    return {
        "status": "success",
        "message": "Rejected reservations synchronized."
    }


# ----------------------------------------------------
# Sync Everything
# ----------------------------------------------------

@app.post("/sync-all")
def sync_all(x_api_key: str = Header(...)):

    validate(x_api_key)

    logger.info("MCP Server | Sync-All request received")

    writer.sync()

    logger.info("MCP Server | Sync-All completed successfully")

    return {
        "status": "success",
        "message": "Reservation files synchronized."
    }