from app.database.sqlite_client import SQLiteClient


class TestSQLiteClient:

    def test_get_available_slot(self):
        """
        Positive Test:
        Ensure at least one slot is available before testing.
        """

        db = SQLiteClient()

        # Arrange
        db.cursor.execute("""
            UPDATE parking_slots
            SET is_available = 1
            WHERE slot_id = 1
        """)
        db.connection.commit()

        # Act
        slot = db.get_available_slot("Jhansi", "Car")

        # Assert
        assert slot is not None
        assert slot["location"] == "Jhansi"

    def test_invalid_reservation_lookup(self):

        db = SQLiteClient()

        reservation = db.get_reservation_by_id(999999)

        assert reservation is None