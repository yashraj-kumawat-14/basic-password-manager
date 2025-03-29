"""
Dialog to handle the "Forgot Password" functionality in the password manager.
"""

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
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from send_otp import EmailSender  # Utility to send OTP via email
from PySide6.QtCore import QTimer
from model.User import User  # User model for database operations

class ForgotPassword(QDialog):
    """
    Dialog class for handling password reset via email and OTP verification.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.otp = -1  # Initialize OTP with an invalid value

        # Set up the dialog window
        self.setWindowTitle("Forgot Password")
        self.setMinimumSize(300, 300)  # Set minimum size for the dialog
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow resizing

        # Email input field
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        
        # OTP input field
        self.otp_label = QLabel("OTP:")
        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("Enter OTP")
        self.otp_input.setEnabled(False)  # Initially disabled

        # Buttons for OTP actions
        self.send_otp_button = QPushButton("Send OTP")
        self.verify_button = QPushButton("Verify OTP")
        self.verify_button.setEnabled(False)  # Initially disabled
        self.resend_otp_button = QPushButton("Resend OTP")
        self.resend_otp_button.setEnabled(False)  # Initially disabled

        # New password input fields
        self.new_password_label = QLabel("New Password:")
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        self.new_password_input.setEnabled(False)  # Initially disabled
        
        self.confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        self.confirm_password_input.setEnabled(False)  # Initially disabled
        
        # Reset password button
        self.reset_password_button = QPushButton("Reset Password")
        self.reset_password_button.setEnabled(False)  # Initially disabled
        self.reset_password_button.setVisible(False)  # Initially hidden

        # Timer for enabling the resend OTP button
        self.timer = QTimer()
        self.timer.setInterval(20000)  # 20 seconds
        self.timer.timeout.connect(self.enable_resend_otp)

        # Connect button signals to their respective slots
        self.send_otp_button.clicked.connect(self.send_otp)
        self.verify_button.clicked.connect(self.verify_otp)
        self.reset_password_button.clicked.connect(self.reset_password)

        # Layout for the dialog
        layout = QVBoxLayout()
        layout.setSpacing(5)  # Decrease vertical spacing between widgets
        layout.setContentsMargins(10, 10, 10, 10)  # Set margins around the layout

        # Add widgets to the layout
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.otp_label)
        layout.addWidget(self.otp_input)
        
        # Button layout for OTP actions
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)  # Decrease horizontal spacing between buttons
        button_layout.addWidget(self.send_otp_button)
        button_layout.addWidget(self.verify_button)
        button_layout.addWidget(self.resend_otp_button)
        
        layout.addLayout(button_layout)
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.reset_password_button)
        
        self.setLayout(layout)

    def send_otp(self):
        """
        Sends an OTP to the user's email.
        """
        email = self.email_input.text()
        if self.validate_email(email):
            # Check if the user exists in the database
            user_exists = User().check_user_exists_by_email(email=email)
            if user_exists:
                # Send OTP via email
                self.otp = EmailSender().send_otp(recipient_email=email)
                QMessageBox.information(self, "Success", "OTP sent to your email!")
                self.send_otp_button.setEnabled(False)  # Disable send OTP button
                self.otp_input.setEnabled(True)  # Enable OTP input
                self.verify_button.setEnabled(True)  # Enable verify button
                self.resend_otp_button.setEnabled(False)  # Disable resend button initially
                self.timer.start()  # Start the timer
            else:
                QMessageBox.critical(self, "Error", "User does not exist for the given email.")
        else:
            QMessageBox.warning(self, "Error", "Please enter a valid email.")

    def verify_otp(self):
        """
        Verifies the entered OTP.
        """
        if str(self.otp) == self.otp_input.text():
            QMessageBox.information(self, "Success", "OTP verified successfully!")
            
            # Disable OTP-related inputs and buttons
            self.otp_input.setEnabled(False)
            self.send_otp_button.setEnabled(False)
            self.verify_button.setEnabled(False)
            self.resend_otp_button.setEnabled(False)
            self.email_input.setEnabled(False)
            
            # Enable new password fields and reset button
            self.new_password_input.setEnabled(True)
            self.confirm_password_input.setEnabled(True)
            self.reset_password_button.setVisible(True)
            self.reset_password_button.setEnabled(True)
        else:
            QMessageBox.critical(self, "Error", "Incorrect OTP. Please try again.")

    def reset_password(self):
        """
        Resets the user's password.
        """
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if new_password and confirm_password:
            if new_password == confirm_password:
                # Update the user's password in the database
                user_id = User().check_user_exists_by_email(email=self.email_input.text())
                User().update_user_password(user_id=user_id, new_password=new_password)
                QMessageBox.information(self, "Success", "Password reset successfully!")
                self.accept()  # Close the dialog
            else:
                QMessageBox.warning(self, "Error", "Passwords do not match. Try again.")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def enable_resend_otp(self):
        """
        Enables the resend OTP button after the timer expires.
        """
        self.resend_otp_button.setEnabled(True)
        self.timer.stop()

    def validate_email(self, email):
        """
        Validates the email format.
        """
        return "@" in email and "." in email

if __name__ == "__main__":
    # Entry point for testing the dialog
    app = QApplication(sys.argv)
    dialog = ForgotPassword()
    dialog.exec()