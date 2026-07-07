from pathlib import Path
import os

from app.database.sqlite_client import SQLiteClient
from app.guardrails.input_filter import Guardrails
from app.utils.logger import logger


os.makedirs("storage", exist_ok=True)


class ReservationWriter:

    def __init__(self):

        self.guard = Guardrails()

        self.storage = Path("data/reservations")
        self.storage.mkdir(parents=True, exist_ok=True)

        self.approved_file = self.storage / "approved_reservations.txt"
        self.rejected_file = self.storage / "rejected_reservations.txt"

    # ----------------------------------------------------
    # Approved Reservations
    # ----------------------------------------------------

    def write_approved_reservations(self):

        db = SQLiteClient()

        try:

            reservations = db.get_approved_reservations()

            with open(self.approved_file, "w", encoding="utf-8") as file:

                file.write("=" * 110 + "\n")
                file.write("SMARTPARK AI - APPROVED RESERVATIONS\n")
                file.write("=" * 110 + "\n")
                file.write("Customer Name | Vehicle Number | Reservation Period | Approval Time\n")
                file.write("-" * 110 + "\n")

                for reservation in reservations:

                    vehicle = self.guard.mask_output(
                        reservation["vehicle_number"]
                    )

                    period = (
                        f"{reservation['reservation_date']} "
                        f"{reservation['start_time']} - "
                        f"{reservation['end_time']}"
                    )

                    approval_time = (
                        reservation["approval_time"]
                        if reservation["approval_time"]
                        else "-"
                    )

                    line = (
                        f"{reservation['first_name']} "
                        f"{reservation['last_name']} | "
                        f"{vehicle} | "
                        f"{period} | "
                        f"{approval_time}"
                    )

                    file.write(line + "\n")

            logger.info(
                f"MCP | Approved reservations synchronized ({len(reservations)} records)"
            )

        finally:

            db.close()

    # ----------------------------------------------------
    # Rejected Reservations
    # ----------------------------------------------------

    def write_rejected_reservations(self):

        db = SQLiteClient()

        try:

            reservations = db.get_rejected_reservations()

            with open(self.rejected_file, "w", encoding="utf-8") as file:

                file.write("=" * 110 + "\n")
                file.write("SMARTPARK AI - REJECTED RESERVATIONS\n")
                file.write("=" * 110 + "\n")
                file.write("Customer Name | Vehicle Number | Reservation Period | Rejection Time\n")
                file.write("-" * 110 + "\n")

                for reservation in reservations:

                    vehicle = self.guard.mask_output(
                        reservation["vehicle_number"]
                    )

                    period = (
                        f"{reservation['reservation_date']} "
                        f"{reservation['start_time']} - "
                        f"{reservation['end_time']}"
                    )

                    rejection_time = (
                        reservation["rejection_time"]
                        if reservation["rejection_time"]
                        else "-"
                    )

                    line = (
                        f"{reservation['first_name']} "
                        f"{reservation['last_name']} | "
                        f"{vehicle} | "
                        f"{period} | "
                        f"{rejection_time}"
                    )

                    file.write(line + "\n")

            logger.info(
                f"MCP | Rejected reservations synchronized ({len(reservations)} records)"
            )

        finally:

            db.close()

    # ----------------------------------------------------
    # Sync Everything
    # ----------------------------------------------------

    def sync(self):

        logger.info("MCP | Synchronization started")

        self.write_approved_reservations()
        self.write_rejected_reservations()

        logger.info("MCP | Synchronization completed successfully")