import os
import smtplib
import ssl

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

print(f"EMAIL    : {EMAIL}")
print(f"PASSWORD : {'SET' if PASSWORD else 'NOT SET'}")

try:

    print("\nSTEP A - Creating SMTP connection")

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587,
        timeout=15
    )

    print("STEP B - SMTP Connected")

    server.ehlo()

    print("STEP C - EHLO Success")

    context = ssl.create_default_context()

    server.starttls(context=context)

    print("STEP D - STARTTLS Success")

    server.ehlo()

    print("STEP E - EHLO After TLS")

    server.login(
        EMAIL,
        PASSWORD
    )

    print("STEP F - Login Success")

    server.sendmail(
        EMAIL,
        EMAIL,
        "Subject: SmartPark Test Email\n\nThis is a test email."
    )

    print("STEP G - Email Sent")

    server.quit()

    print("STEP H - Connection Closed")

    print("\n✅ SUCCESS")

except Exception as e:

    print("\n❌ ERROR")
    print(type(e).__name__)
    print(e)