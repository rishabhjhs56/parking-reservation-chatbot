import sqlite3

DB_PATH = "database/parking.db"


class SQLiteClient:

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    # -----------------------------------------
    # Find first available slot
    # -----------------------------------------

    def get_available_slot(self, location, vehicle_type):

        self.cursor.execute(
            """
            SELECT *
            FROM parking_slots
           WHERE LOWER(location) = LOWER(?) 
        AND LOWER(vehicle_type) = LOWER(?)
            AND is_available = 1
            LIMIT 1
            """,
            (location, vehicle_type)
        )

        return self.cursor.fetchone()

    # -----------------------------------------
    # Reserve slot
    # -----------------------------------------

    def reserve_slot(self, slot_id):

        self.cursor.execute(
            """
            UPDATE parking_slots
            SET is_available = 0
            WHERE slot_id = ?
            """,
            (slot_id,)
        )

        self.connection.commit()

    # -----------------------------------------
    # Release slot
    # -----------------------------------------

    def release_slot(self, slot_id):

        self.cursor.execute(
            """
            UPDATE parking_slots
            SET is_available = 1
            WHERE slot_id = ?
            """,
            (slot_id,)
        )

        self.connection.commit()

    # -----------------------------------------
    # Save reservation
    # -----------------------------------------

    def save_reservation(self, reservation):

        self.cursor.execute(
            """
            INSERT INTO reservations
            (
                first_name,
                last_name,
                phone_number,
                vehicle_number,
                vehicle_type,
                driving_license,
                location,
                reservation_date,
                start_time,
                end_time,
                slot_id,
                status
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (

                reservation.first_name,
                reservation.last_name,
                reservation.phone_number,
                reservation.vehicle_number,
                reservation.vehicle_type,
                reservation.driving_license,
                reservation.location,
                reservation.reservation_date,
                reservation.start_time,
                reservation.end_time,
                reservation.slot_id,
                reservation.status

            )

        )

        self.connection.commit()

        return self.cursor.lastrowid

    # -----------------------------------------
    # Pending reservations
    # -----------------------------------------

    def get_pending_reservations(self):

        self.cursor.execute(
            """
            SELECT *
            FROM reservations
            WHERE status='PENDING'
            """
        )

        return self.cursor.fetchall()

    # -----------------------------------------
    # Approve reservation
    # -----------------------------------------

    def approve_reservation(self, reservation_id):

        self.cursor.execute(
            """
            UPDATE reservations
            SET status='APPROVED'
            WHERE reservation_id=?
            """,
            (reservation_id,)
        )

        self.connection.commit()

    # -----------------------------------------
    # Reject reservation
    # -----------------------------------------

    def reject_reservation(self, reservation_id):

        slot_id = self.get_slot_id(reservation_id)

        self.cursor.execute(
            """
            UPDATE reservations
            SET status='REJECTED'
            WHERE reservation_id=?
            """,
            (reservation_id,)
        )

        if slot_id:
            self.cursor.execute(
                """
                UPDATE parking_slots
                SET is_available=1
                WHERE slot_id=?
                """,
                (slot_id,)
            )

        self.connection.commit()

    # -----------------------------------------

    # -----------------------------------------
# Get Reservation By ID
# -----------------------------------------

    def get_reservation_by_id(self, reservation_id):
        self.cursor.execute(
        """
        SELECT *
        FROM reservations
        WHERE reservation_id = ?
        """,
        (reservation_id,))

        return self.cursor.fetchone()
    
    def pending_reservation(self, reservation_id):

        slot_id = self.get_slot_id(reservation_id)

        self.cursor.execute(
            """
            UPDATE reservations
            SET status='PENDING'
            WHERE reservation_id=?
            """,
            (reservation_id,)
        )

        if slot_id:
            self.cursor.execute(
                """
                UPDATE parking_slots
                SET is_available=0
                WHERE slot_id=?
                """,
                (slot_id,)
            )

        self.connection.commit()


    def get_slot_id(self, reservation_id):

        self.cursor.execute(
            """
            SELECT slot_id
            FROM reservations
            WHERE reservation_id=?
            """,
            (reservation_id,)
        )

        row = self.cursor.fetchone()

        if row:
            return row["slot_id"]

        return None

    def close(self):
        self.connection.close()