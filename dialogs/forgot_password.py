import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QSizePolicy
)

import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from send_otp import EmailSender 

from PySide6.QtCore import QTimer
from model.User import User

class ForgotPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.otp=-1

        self.setWindowTitle("Forgot Password")
        self.setMinimumSize(300, 200)  # Set minimum size for the dialog
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow resizing

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        
        self.otp_label = QLabel("OTP:")
        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("Enter OTP")
        self.otp_input.setEnabled(False)  # Initially disabled

        self.send_otp_button = QPushButton("Send OTP")
        self.verify_button = QPushButton("Verify OTP")
        self.verify_button.setEnabled(False)  # Initially disabled
        self.resend_otp_button = QPushButton("Resend OTP")
        self.resend_otp_button.setEnabled(False)  # Initially disabled

        self.timer = QTimer()
        self.timer.setInterval(20000)  # 20 seconds
        self.timer.timeout.connect(self.enable_resend_otp)

        self.send_otp_button.clicked.connect(self.send_otp)
        self.verify_button.clicked.connect(self.verify_otp)

        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.otp_label)
        layout.addWidget(self.otp_input)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_otp_button)
        button_layout.addWidget(self.verify_button)
        button_layout.addWidget(self.resend_otp_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def send_otp(self):
        email = self.email_input.text()
        if self.validate_email(email):
            # Simulate sending OTP
            user_exists = User().check_user_exists_by_email(email=email)
            print("user exists = ", user_exists)
            if(user_exists):
                self.otp = EmailSender().send_otp(recipient_email=email)
                print(self.otp)
                QMessageBox.information(self, "Success", "OTP sent to your email!")
                self.send_otp_button.setEnabled(False)
                self.otp_input.setEnabled(True)  # Enable OTP input
                self.verify_button.setEnabled(True)  # Enable verify button
                self.resend_otp_button.setEnabled(False)  # Disable resend button initially
                self.timer.start()  # Start the timer
            else:
                QMessageBox.critical(self, "User don't exist", "User doesn't exist for the given email. Retry again.")
        else:
            QMessageBox.warning(self, "Error", "Please enter a valid email.")

    def verify_otp(self):
        # Here you would implement the actual OTP verification logic
        if(str(self.otp)==self.otp_input.text()):
            print("otp verified")
        else:
            QMessageBox.critical(self, "Wrong OTP", "OTP was wrong try again.")
            

    def enable_resend_otp(self):
        self.resend_otp_button.setEnabled(True)
        self.timer.stop()

    def validate_email(self, email):
        # Simple email validation
        return "@" in email and "." in email

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ForgotPassword()
    dialog.exec()