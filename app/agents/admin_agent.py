from app.database.sqlite_client import SQLiteClient
from app.guardrails.input_filter import Guardrails
from app.utils.email_service import EmailService
from app.utils.logger import logger


class AdminAgent:

    def __init__(self):
        self.db = SQLiteClient()
        self.guard = Guardrails()
        self.email = EmailService()

    # ----------------------------------------
    # Show Pending Reservations
    # ----------------------------------------

    def show_pending_reservations(self):

        reservations = self.db.get_pending_reservations()

        if not reservations:
            print("\n✅ No pending reservations.\n")
            return

        print("\n========== Pending Reservations ==========\n")

        for reservation in reservations:

            print(f"Reservation ID : {reservation['reservation_id']}")
            print(f"Customer       : {reservation['first_name']} {reservation['last_name']}")
            print(f"Location       : {reservation['location']}")

            print(
                f"Phone          : {self.guard.mask_output(reservation['phone_number'])}"
            )

            print(
                f"Vehicle        : {reservation['vehicle_type']} ({self.guard.mask_output(reservation['vehicle_number'])})"
            )

            print(
                f"Driving Licence: {self.guard.mask_output(reservation['driving_license'])}"
            )

            print(f"Slot ID        : {reservation['slot_id']}")
            print(f"Status         : {reservation['status']}")
            print("-" * 45)

    # ----------------------------------------
    # Approve Reservation
    # ----------------------------------------

    def approve_reservation(self, reservation_id):

        reservation = self.db.get_reservation_by_id(reservation_id)

        if reservation is None:
            print(f"\n❌ Reservation {reservation_id} not found.\n")
            return

        self.db.approve_reservation(reservation_id)

        reservation = self.db.get_reservation_by_id(reservation_id)

        self.email.send_approval_email(reservation)

        logger.info(
            f"Reservation Approved | ReservationID={reservation_id}"
        )

        print(f"\n✅ Reservation {reservation_id} Approved.\n")

    # ----------------------------------------
    # Reject Reservation
    # ----------------------------------------

    def reject_reservation(self, reservation_id):

        reservation = self.db.get_reservation_by_id(reservation_id)

        if reservation is None:
            print(f"\n❌ Reservation {reservation_id} not found.\n")
            return

        self.db.reject_reservation(reservation_id)

        reservation = self.db.get_reservation_by_id(reservation_id)

        self.email.send_rejection_email(reservation)

        logger.info(
            f"Reservation Rejected | ReservationID={reservation_id}"
        )

        print(f"\n❌ Reservation {reservation_id} Rejected.\n")

    # ----------------------------------------
    # Notify Admin
    # ----------------------------------------

    def notify_admin(self, reservation):

        print("\n" + "=" * 60)
        print("📨 NEW RESERVATION REQUEST RECEIVED")
        print("=" * 60)

        print(f"Customer : {reservation.first_name} {reservation.last_name}")
        print(f"Location : {reservation.location}")
        print(f"Vehicle  : {reservation.vehicle_type}")
        print(f"Date     : {reservation.reservation_date}")
        print(f"Time     : {reservation.start_time} - {reservation.end_time}")
        print(f"Slot     : {reservation.zone}-{reservation.block}-{reservation.slot_number}")

        print("=" * 60 + "\n")

        logger.info(
            f"Admin Notified | ReservationID={reservation.reservation_id}"
        )

        masked_phone = self.guard.mask_output(reservation.phone_number)
        masked_vehicle = self.guard.mask_output(reservation.vehicle_number)
        masked_dl = self.guard.mask_output(reservation.driving_license)

        self.email.send_admin_notification(
            reservation,
            masked_phone,
            masked_vehicle,
            masked_dl
        )