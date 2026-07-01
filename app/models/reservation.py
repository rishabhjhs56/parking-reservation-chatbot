from dataclasses import dataclass


@dataclass
class Reservation:

    first_name: str = ""
    last_name: str = ""
    vehicle_number: str = ""
    vehicle_type: str = ""
    reservation_date: str = ""
    start_time: str = ""
    end_time: str = ""
    status: str = "Pending"