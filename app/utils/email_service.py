import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.utils.logger import logger
from app.utils.config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    ADMIN_EMAIL,
)


class EmailService:

    # -------------------------------------------------
    # Common Email Sender
    # -------------------------------------------------

    def _send_email(self, subject, body, html=False):

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = ADMIN_EMAIL
        message["Subject"] = subject

        if html:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))

        try:

            #print("EMAIL STEP 1 - Connecting")

            server = smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465,
                timeout=20
            )

            #print("EMAIL STEP 2 - Connected")

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            #print("EMAIL STEP 3 - Logged In")

            server.send_message(message)

            #print("EMAIL STEP 4 - Email Sent")

            server.quit()

            #print("EMAIL STEP 5 - Connection Closed")

            return True

        except Exception as e:

            print(f"❌ Email Error: {e}")

            logger.error(
                f"Email Sending Failed | Error={e}"
            )

            return False

    # -------------------------------------------------
    # Send Reservation To Admin
    # -------------------------------------------------

    def send_admin_notification(
        self,
        reservation,
        masked_phone,
        masked_vehicle,
        masked_dl
    ):

        subject = (
            f"🚗 New Parking Reservation "
            f"#{reservation.reservation_id}"
        )

        approve_link = (
            f"http://127.0.0.1:5000/approve/"
            f"{reservation.reservation_id}"
        )

        reject_link = (
            f"http://127.0.0.1:5000/reject/"
            f"{reservation.reservation_id}"
        )

        pending_link = (
            f"http://127.0.0.1:5000/pending/"
            f"{reservation.reservation_id}"
        )

        html = f"""
<html>

<body style="font-family:Arial">

<h2>🚗 New Parking Reservation</h2>

<hr>

<p><b>Reservation ID:</b> {reservation.reservation_id}</p>

<p><b>Customer:</b> {reservation.first_name} {reservation.last_name}</p>

<p><b>Location:</b> {reservation.location}</p>

<p><b>Zone:</b> {reservation.zone}</p>

<p><b>Block:</b> {reservation.block}</p>

<p><b>Slot:</b> {reservation.slot_number}</p>

<p><b>Vehicle Type:</b> {reservation.vehicle_type}</p>

<p><b>Vehicle Number:</b> {masked_vehicle}</p>

<p><b>Phone:</b> {masked_phone}</p>

<p><b>Driving Licence:</b> {masked_dl}</p>

<p><b>Date:</b> {reservation.reservation_date}</p>

<p><b>Time:</b> {reservation.start_time} -
{reservation.end_time}</p>

<p><b>Status:</b> {reservation.status}</p>

<hr>

<a href="{approve_link}"
style="background:#28a745;
color:white;
padding:12px 20px;
text-decoration:none;
border-radius:5px;">
✅ APPROVE
</a>

&nbsp;&nbsp;

<a href="{reject_link}"
style="background:#dc3545;
color:white;
padding:12px 20px;
text-decoration:none;
border-radius:5px;">
❌ REJECT
</a>

&nbsp;&nbsp;

<a href="{pending_link}"
style="background:#ffc107;
color:black;
padding:12px 20px;
text-decoration:none;
border-radius:5px;">
🟡 REVERT TO PENDING
</a>

</body>

</html>
"""

        success = self._send_email(
            subject,
            html,
            html=True
        )

        if success:

            logger.info(
                f"Admin Email Sent | "
                f"ReservationID={reservation.reservation_id}"
            )

            print("✅ Admin email sent successfully.")

    # -------------------------------------------------
    # Approval Email
    # -------------------------------------------------

    def send_approval_email(self, reservation):

        subject = (
            f"✅ Reservation "
            f"#{reservation['reservation_id']} Approved"
        )

        body = f"""
Hello,

Reservation has been APPROVED.

Reservation ID : {reservation['reservation_id']}
Customer       : {reservation['first_name']} {reservation['last_name']}
Location       : {reservation['location']}
Status         : APPROVED

Regards,
SmartPark AI
"""

        success = self._send_email(subject, body)

        if success:

            logger.info(
                f"Approval Email Sent | "
                f"ReservationID={reservation['reservation_id']}"
            )

    # -------------------------------------------------
    # Rejection Email
    # -------------------------------------------------

    def send_rejection_email(self, reservation):

        subject = (
            f"❌ Reservation "
            f"#{reservation['reservation_id']} Rejected"
        )

        body = f"""
Hello,

Reservation has been REJECTED.

Reservation ID : {reservation['reservation_id']}
Customer       : {reservation['first_name']} {reservation['last_name']}
Location       : {reservation['location']}
Status         : REJECTED

Regards,
SmartPark AI
"""

        success = self._send_email(subject, body)

        if success:

            logger.info(
                f"Rejection Email Sent | "
                f"ReservationID={reservation['reservation_id']}"
            )