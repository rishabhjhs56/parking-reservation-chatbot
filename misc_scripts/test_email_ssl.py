import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

try:
    print("Connecting using SMTP_SSL...")

    server = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        timeout=15
    )

    print("Connected")

    server.login(EMAIL, PASSWORD)

    print("Login Success")

    server.sendmail(
        EMAIL,
        EMAIL,
        "Subject: Test\n\nHello"
    )

    print("Email Sent")

    server.quit()

except Exception as e:
    print(type(e).__name__)
    print(e)