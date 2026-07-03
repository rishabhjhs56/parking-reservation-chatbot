import re
from datetime import datetime
from app.models.reservation import Reservation
from app.database.sqlite_client import SQLiteClient
from app.guardrails.input_filter import Guardrails
from app.agents.admin_agent import AdminAgent
from app.utils.logger import logger

class ReservationAgent:
    def __init__(self):
        self.reservation = None
        self.step = None
        self.db = SQLiteClient()
        self.guard = Guardrails()
        self.admin = AdminAgent()

    def reset_agent(self):
        """Clears state parameters for next reservation sessions."""
        self.reservation = None
        self.step = None

    def start_reservation(self, prefilled_location=None) -> str:
        """
        Initializes the reservation state. Skip location prompt if already provided.
        """
        self.reservation = Reservation()
        
        # Safe default attribute initialization in case model has missing fields
        if not hasattr(self.reservation, "location"):
            self.reservation.location = None
        if not hasattr(self.reservation, "phone_number"):
            self.reservation.phone_number = None

        if prefilled_location:
            self.reservation.location = prefilled_location
            self.step = "first_name"
            return f"📍 Great! I've set your location to **{prefilled_location}**.\nLet's start your booking. (Type 'cancel' at any time to exit).\n\nWhat is your first name?"
        
        self.step = "location"
        return "Great! Let's start your parking reservation.\n(Type 'cancel' at any time to exit).\n\nWhich location do you want to book? (Delhi, Mumbai, Bengaluru, Hyderabad, Noida, Pune, Jhansi)"

    # ---------------- VALIDATIONS ----------------
    def is_valid_location(self, text: str) -> bool:
        valid_locations = ["jhansi", "delhi", "mumbai", "bkc", "bengaluru", "noida", "pune", "hyderabad", "whitefield", "hitech city"]
        return text.lower().strip() in valid_locations

    def is_valid_name(self, text: str) -> bool:
        return bool(re.match(r"^[A-Za-z ]{2,30}$", text.strip()))

    def is_valid_phone(self, text: str) -> bool:
        clean_text = text.replace(" ", "").replace("-", "")
        return bool(re.match(r"^\d{10}$", clean_text))
    
    def is_valid_driving_license(self, text: str) -> bool:
        """Basic Indian Driving Licence validation. Example: UP3220210001234"""
        clean_text = text.replace(" ", "").upper()
        return bool(re.match(r"^[A-Z]{2}[0-9]{2}[0-9]{4}[0-9]{7}$",clean_text))

    def is_valid_vehicle(self, text: str) -> bool:
        clean_text = text.replace(" ", "").replace("-", "")
        return bool(re.match(r"^[A-Za-z0-9]{4,15}$", clean_text))

    def is_valid_vehicle_type(self, text: str) -> bool:
        return text.lower() in ["car", "suv", "motorcycle", "ev"]

    def is_valid_date(self, text: str) -> bool:
        try:
            parsed_date = datetime.strptime(text, "%Y-%m-%d").date()
            # Ensure booking date is not in the past
            if parsed_date < datetime.now().date():
                return False
            return True
        except ValueError:
            return False

    def is_valid_time(self, text: str) -> bool:
        try:
            datetime.strptime(text, "%H:%M")
            return True
        except ValueError:
            return False

    # ---------------- STEP BY STEP FLOW ----------------
    def handle_input(self, user_input: str) -> str:
        user_input = user_input.strip()

        # Step: Location
        if self.step == "location":
            if not self.is_valid_location(user_input):
                return "❌ We don't operate in that location. Choose: Delhi, Mumbai, Bengaluru, Hyderabad, Noida, Pune, or Jhansi."
            self.reservation.location = user_input.title()
            self.step = "first_name"
            return f"📍 Location set to {user_input.title()}. What is your first name?"

        # Step: First Name
        elif self.step == "first_name":
            if not self.is_valid_name(user_input):
                return "❌ Invalid name. Please use letters only (2-30 characters)."
            self.reservation.first_name = user_input.capitalize()
            self.step = "last_name"
            return "Thanks! What is your last name?"

        # Step: Last Name
        elif self.step == "last_name":
            if not self.is_valid_name(user_input):
                return "❌ Invalid last name. Please use letters only (2-30 characters)."
            self.reservation.last_name = user_input.capitalize()
            self.step = "phone_number"
            return "Please enter your 10-digit mobile number (e.g., 9876543210):"

        # Step: Phone Number
        elif self.step == "phone_number":
            clean_phone = user_input.replace(" ", "").replace("-", "")
            if not self.is_valid_phone(clean_phone):
                return "❌ Invalid mobile number. Please enter exactly 10 digits without symbols."
            self.reservation.phone_number = clean_phone
            self.step = "vehicle_number"
            return "Got it. What is your vehicle plate number? (e.g., MH01AB1234)"

        # Step: Vehicle  Number
        elif self.step == "vehicle_number":
            clean_plate = user_input.replace(" ", "").replace("-", "").upper()
            if not self.is_valid_vehicle(clean_plate):
                return "❌ Invalid license plate. Enter alphanumeric characters only."
            self.reservation.vehicle_number = clean_plate
            self.step = "driving_license"
            return "Please enter your 15 digit driving license number or any government-issued ID (alphanumeric, no spaces or symbols FOR EG. TN1020189876543):"
        
        elif self.step == "driving_license":
            clean_dl = user_input.replace(" ", "").replace("-", "").upper()
            if not self.is_valid_driving_license(clean_dl):
                return "❌ Invalid driving license. Enter alphanumeric characters only."
            self.reservation.driving_license=clean_dl
            self.step = "vehicle_type"
            return "What type of vehicle is it? (Choose: Car, SUV, Motorcycle, or EV)"

        # Step: Vehicle Type
        elif self.step == "vehicle_type":
            if not self.is_valid_vehicle_type(user_input):
                return "❌ Invalid selection. Choose: Car, SUV, Motorcycle, or EV."
            self.reservation.vehicle_type = user_input.title()
            self.step = "reservation_date"
            return "Which date would you like to book? (Format: YYYY-MM-DD, e.g., 2026-07-05)"

        # Step: Reservation Date
        elif self.step == "reservation_date":
            if not self.is_valid_date(user_input):
                return "❌ Invalid date. Ensure format is YYYY-MM-DD and it's a current or future date."
            self.reservation.reservation_date = user_input
            self.step = "start_time"
            return "What time will your reservation start? (Format 24-hour: HH:MM, e.g., 14:30)"

        # Step: Start Time
        elif self.step == "start_time":
            if not self.is_valid_time(user_input):
                return "❌ Invalid time format. Please write in 24-hour HH:MM format (e.g., 09:30)."
            self.reservation.start_time = user_input
            self.step = "end_time"
            return "What time will your reservation end? (Format 24-hour: HH:MM, e.g., 18:00)"

        # Step: End Time (Finalization)

        elif self.step == "end_time":
            if not self.is_valid_time(user_input):
                return "❌ Invalid time format. Please write in 24-hour HH:MM format (e.g., 17:00)."
            self.reservation.end_time = user_input

            if user_input <= self.reservation.start_time:
                return "❌ End time must be after the start time. Please enter a valid end time."
            # ----------------------------------------
            # Allocate Parking Slot
            #----------------------------------------
            slot = self.db.get_available_slot(self.reservation.location,self.reservation.vehicle_type)

            if slot is None:
                logger.warning(
        f"No Slot Available | "
        f"Location={self.reservation.location} | "
        f"VehicleType={self.reservation.vehicle_type}"
    )

                self.reset_agent()
                return "❌ Sorry! No parking slots are available."
            
            self.reservation.slot_id = slot["slot_id"]
            self.reservation.zone = slot["zone"]
            self.reservation.block = slot["block"]
            self.reservation.slot_number = slot["slot_number"]

            # ----------------------------------------
            # Reserve Slot
            # ----------------------------------------

            self.db.reserve_slot(slot["slot_id"])

            # ----------------------------------------
            # Save Reservation
            # ----------------------------------------

            reservation_id = self.db.save_reservation(self.reservation)
            self.reservation.reservation_id = reservation_id
            logger.info(
        f"Reservation Created | "
        f"ReservationID={reservation_id} | "
        f"Customer={self.reservation.first_name} {self.reservation.last_name} | "
        f"Location={self.reservation.location} | "
        f"Vehicle={self.reservation.vehicle_number}"
)
            self.admin.notify_admin(self.reservation)
            self.step = "done"
            return self.get_summary()
        else:
            return "This reservation session is already completed."

    def get_summary(self) -> str:
        """
        Builds a final confirmation receipt and resets the state.
        """
        masked_vehicle = self.guard.mask_output(getattr(self.reservation, "vehicle_number", ""))
        masked_phone = self.guard.mask_output(getattr(self.reservation, "phone_number", ""))
        masked_dl = self.guard.mask_output(getattr(self.reservation, "driving_license", ""))


        summary = f"""
🎉 Reservation Completed Successfully!

🆔 Reservation ID: {getattr(self.reservation, 'reservation_id', 'Not Generated')}
🗺️ Zone: {getattr(self.reservation, 'zone', 'Not Assigned')}
🏢 Block: {getattr(self.reservation, 'block', 'Not Assigned')}
🅿️ Slot: {getattr(self.reservation, 'slot_number', 'Not Assigned')}
📍 Location: {getattr(self.reservation, 'location', 'Not Set')}
👤 Name: {self.reservation.first_name} {self.reservation.last_name}
📱 Phone: {masked_phone}
🚗 Vehicle: {self.reservation.vehicle_type} ({masked_vehicle})
🪪 Driving Licence: {masked_dl}
📅 Date: {self.reservation.reservation_date}
⏰ Time: {self.reservation.start_time} - {self.reservation.end_time}

Status: Pending Admin Approval ⏳
"""
        self.reset_agent()
        return summary      