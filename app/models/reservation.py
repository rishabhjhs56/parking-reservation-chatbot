from dataclasses import dataclass

@dataclass
class Reservation:

    first_name: str = ""
    last_name: str = ""
    phone_number: str = ""

    vehicle_number: str = ""
    vehicle_type: str = ""

    reservation_date: str = ""
    start_time: str = ""
    end_time: str = ""

    location: str = ""

    driving_license: str = ""

    reservation_id: int = 0

    slot_id: int = 0

    zone: str = ""

    block: str = ""

    slot_number: str = ""

    status: str = "PENDING"

    admin_comments: str = ""