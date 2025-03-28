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
from PySide6.QtCore import QTimer

class ForgotPassword(QDialog):
    def __init__(self):
        super().__init__()

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
            QMessageBox.information(self, "Success", "OTP sent to your email!")
            self.send_otp_button.setEnabled(False)
            self.otp_input.setEnabled(True)  # Enable OTP input
            self.verify_button.setEnabled(True)  # Enable verify button
            self.resend_otp_button.setEnabled(False)  # Disable resend button initially
            self.timer.start()  # Start the timer
        else:
            QMessageBox.warning(self, "Error", "Please enter a valid email.")

    def verify_otp(self):
        # Here you would implement the actual OTP verification logic
        QMessageBox.information(self, "Verify", "OTP verification logic goes here.")

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