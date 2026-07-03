import sqlite3

DB_PATH = "database/parking.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

slots = [

    # ---------------- Jhansi ----------------
    ("Jhansi", "A", "A", "A01", "CAR", 10),
    ("Jhansi", "A", "A", "A02", "CAR", 10),
    ("Jhansi", "A", "A", "A03", "EV", 10),
    ("Jhansi", "B", "B", "B01", "SUV", 10),
    ("Jhansi", "C", "C", "C01", "MOTORCYCLE", 1),

    # ---------------- Delhi ----------------
    ("Delhi", "A", "A", "A01", "CAR", 1),
    ("Delhi", "A", "A", "A02", "EV", 1),
    ("Delhi", "B", "B", "B01", "SUV", 1),
    ("Delhi", "C", "C", "C01", "MOTORCYCLE", 1),

    # ---------------- Mumbai ----------------
    ("Mumbai", "A", "A", "A01", "CAR", 1),
    ("Mumbai", "A", "A", "A02", "EV", 1),
    ("Mumbai", "B", "B", "B01", "SUV", 1),
    ("Mumbai", "C", "C", "C01", "MOTORCYCLE", 1),

    # ---------------- Bengaluru ----------------
    ("Bengaluru", "A", "A", "A01", "CAR", 1),
    ("Bengaluru", "A", "A", "A02", "EV", 1),
    ("Bengaluru", "B", "B", "B01", "SUV", 1),
    ("Bengaluru", "C", "C", "C01", "MOTORCYCLE", 1),

    # ---------------- Hyderabad ----------------
    ("Hyderabad", "A", "A", "A01", "CAR", 1),
    ("Hyderabad", "A", "A", "A02", "EV", 1),
    ("Hyderabad", "B", "B", "B01", "SUV", 1),
    ("Hyderabad", "C", "C", "C01", "MOTORCYCLE", 1),

    # ---------------- Pune ----------------
    ("Pune", "A", "A", "A01", "CAR", 10),
    ("Pune", "A", "A", "A02", "EV", 1),
    ("Pune", "B", "B", "B01", "SUV", 1),
    ("Pune", "C", "C", "C01", "MOTORCYCLE", 10),

    # ---------------- Noida ----------------
    ("Noida", "A", "A", "A01", "CAR", 1),
    ("Noida", "A", "A", "A02", "EV", 1),
    ("Noida", "B", "B", "B01", "SUV", 1),
    ("Noida", "C", "C", "C01", "MOTORCYCLE", 1),
]

cursor.executemany(
    """
    INSERT INTO parking_slots
    (
        location,
        zone,
        block,
        slot_number,
        vehicle_type,
        is_available
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    slots,
)

conn.commit()
conn.close()

print("✅ Parking slots inserted successfully.")