import yagmail
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.yag = yagmail.SMTP(self.sender_email, self.sender_password)
        self.currentOtp = None  # Stores the latest OTP sent

    def send_email(self, recipient_email, subject, body):
        try:
            self.yag.send(recipient_email, subject, body)
            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_otp(self, recipient_email):
        self.currentOtp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        subject = "Your OTP Code"
        body = f"Your OTP is: {self.currentOtp}"
        self.send_email(recipient_email, subject, body)
        return self.currentOtp  # Returning OTP for verification use

# Example Usage
email_sender = EmailSender()
otp = email_sender.send_otp("recipient@example.com")
print(f"OTP sent: {otp}")
