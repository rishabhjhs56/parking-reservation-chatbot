from flask import Flask

from app.database.sqlite_client import SQLiteClient
from app.mcp.client import MCPClient
from app.utils.logger import logger

app = Flask(__name__)


@app.route("/")
def home():
    logger.info("Admin API | Health Check")
    return "SmartPark Admin API Running"


# ----------------------------------------------------
# Approve Reservation
# ----------------------------------------------------

@app.route("/approve/<int:reservation_id>")
def approve(reservation_id):

    db = SQLiteClient()

    try:

        reservation = db.get_reservation_by_id(reservation_id)

        if reservation is None:

            logger.warning(
                f"Admin API | Approve failed | ReservationID={reservation_id}"
            )

            return f"<h2>❌ Reservation {reservation_id} not found.</h2>", 404

        db.approve_reservation(reservation_id)

        logger.info(
            f"Admin API | Reservation Approved | ReservationID={reservation_id}"
        )

        MCPClient().sync_all()

        logger.info(
            f"Admin API | MCP Sync Completed | ReservationID={reservation_id}"
        )

        return f"""
        <h2>✅ Reservation {reservation_id} Approved Successfully</h2>

        <a href="/pending/{reservation_id}">
            Revert To Pending
        </a>
        """

    finally:
        db.close()


# ----------------------------------------------------
# Reject Reservation
# ----------------------------------------------------

@app.route("/reject/<int:reservation_id>")
def reject(reservation_id):

    db = SQLiteClient()

    try:

        reservation = db.get_reservation_by_id(reservation_id)

        if reservation is None:

            logger.warning(
                f"Admin API | Reject failed | ReservationID={reservation_id}"
            )

            return f"<h2>❌ Reservation {reservation_id} not found.</h2>", 404

        db.reject_reservation(reservation_id)

        logger.info(
            f"Admin API | Reservation Rejected | ReservationID={reservation_id}"
        )

        MCPClient().sync_all()

        logger.info(
            f"Admin API | MCP Sync Completed | ReservationID={reservation_id}"
        )

        return f"""
        <h2>❌ Reservation {reservation_id} Rejected Successfully</h2>

        <a href="/pending/{reservation_id}">
            Revert To Pending
        </a>
        """

    finally:
        db.close()


# ----------------------------------------------------
# Revert Reservation to Pending
# ----------------------------------------------------

@app.route("/pending/<int:reservation_id>")
def pending(reservation_id):

    db = SQLiteClient()

    try:

        reservation = db.get_reservation_by_id(reservation_id)

        if reservation is None:

            logger.warning(
                f"Admin API | Pending failed | ReservationID={reservation_id}"
            )

            return f"<h2>❌ Reservation {reservation_id} not found.</h2>", 404

        db.pending_reservation(reservation_id)

        logger.info(
            f"Admin API | Reservation Moved To Pending | ReservationID={reservation_id}"
        )

        MCPClient().sync_all()

        logger.info(
            f"Admin API | MCP Sync Completed | ReservationID={reservation_id}"
        )

        return f"""
        <h2>🟡 Reservation {reservation_id} moved back to Pending.</h2>
        """

    finally:
        db.close()


# ----------------------------------------------------
# Run Flask
# ----------------------------------------------------

if __name__ == "__main__":

    logger.info("Admin API Started")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )