
from pathlib import Path
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from app.utils.config import FASTAPI_MCP_API_KEY
from app.mcp.server import app



client = TestClient(app)

VALID_API_KEY = FASTAPI_MCP_API_KEY
INVALID_API_KEY = "invalid-api-key"

EXPORT_DIR = Path("data/reservations")
APPROVED_FILE = EXPORT_DIR / "approved_reservations.txt"
REJECTED_FILE = EXPORT_DIR / "rejected_reservations.txt"


# ----------------------------------------------------
# TC-01
# Verify successful synchronization
# ----------------------------------------------------

def test_mcp_sync_success():

    response = client.post(
        "/sync-all",
        headers={
            "x-api-key": VALID_API_KEY
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "success",
        "message": "Reservation files synchronized."
    }

    assert APPROVED_FILE.exists()
    assert REJECTED_FILE.exists()


# ----------------------------------------------------
# TC-02
# Verify unauthorized request
# ----------------------------------------------------

def test_mcp_sync_invalid_api_key():

    response = client.post(
        "/sync-all",
        headers={
            "x-api-key": INVALID_API_KEY
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Unauthorized"
    }


# ----------------------------------------------------
# TC-03
# Verify Approved Reservation file is generated
# ----------------------------------------------------

def test_approved_reservation_file_created():

    client.post(
        "/sync-approved",
        headers={
            "x-api-key": VALID_API_KEY
        }
    )

    assert APPROVED_FILE.exists()

    assert APPROVED_FILE.stat().st_size > 0


# ----------------------------------------------------
# TC-04
# Verify Approved Reservation file structure
# ----------------------------------------------------

def test_approved_reservation_file_structure():

    client.post(
        "/sync-approved",
        headers={
            "x-api-key": VALID_API_KEY
        }
    )

    assert APPROVED_FILE.exists()

    with open(APPROVED_FILE, "r", encoding="utf-8") as file:

        content = file.readlines()

    assert len(content) >= 5

    assert "SMARTPARK AI - APPROVED RESERVATIONS" in content[1]

    assert "Customer Name" in content[3]

    assert "Vehicle Number" in content[3]

    assert "Reservation Period" in content[3]

    assert "Approval Time" in content[3]

    assert "|" in content[-1]