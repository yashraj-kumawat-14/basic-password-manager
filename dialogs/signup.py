# Signup Dialog to display signup window to user

# Importing necessary modules and libraries
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QApplication, QGridLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
import sys
import os

# Add the project root to sys.path to allow importing modules from the project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Importing the User model to handle user-related operations
from model.User import User

# Signup class for displaying signup window and handling the logic of signup
class Signup(QDialog):
    def __init__(self, parent=None):
        # Initialize the QDialog class
        super().__init__(parent)
        
        # Set the geometry of the signup window
        self.setGeometry(100, 100, 350, 170)
        
        # Set the title of the signup window
        self.setWindowTitle("Signup")
        
        # Create a grid layout for organizing widgets
        layout = QGridLayout()
        
        # Create a message label for displaying error or success messages
        self.message_label = QLabel("Create a new account")
        
        # Create labels for input fields
        username_label = QLabel("Username :")
        email_label = QLabel("Email :")
        password_label = QLabel("Password :")
        confirm_password_label = QLabel("Confirm Password :")
        
        # Create input fields for user details
        self.username_entry = QLineEdit()
        self.email_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.confirm_password_entry = QLineEdit()
        
        # Create a signup button and connect it to the registerUser method
        signup_button = QPushButton("Sign Up")
        signup_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        signup_button.clicked.connect(self.registerUser)
        
        # Set styles and alignments for labels and message label
        self.message_label.setStyleSheet("color: Black; font-size: 19px; padding:10px")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        email_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        password_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        confirm_password_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Add widgets to the layout
        layout.addWidget(self.message_label, 0, 0, 1, 3)
        layout.addWidget(username_label, 1, 0, 1, 1)
        layout.addWidget(self.username_entry, 1, 1, 1, 2)
        layout.addWidget(email_label, 2, 0, 1, 1)
        layout.addWidget(self.email_entry, 2, 1, 1, 2)
        layout.addWidget(password_label, 3, 0, 1, 1)
        layout.addWidget(self.password_entry, 3, 1, 1, 2)
        layout.addWidget(confirm_password_label, 4, 0, 1, 1)
        layout.addWidget(self.confirm_password_entry, 4, 1, 1, 2)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 5, 0, 1, 3)
        layout.addWidget(signup_button, 6, 0, 1, 3)
        
        # Set the layout for the dialog
        self.setLayout(layout)
    
    # Method to handle user registration
    def registerUser(self):
        # Get user input from the fields
        username = self.username_entry.text().strip()
        email = self.email_entry.text().strip()
        password = self.password_entry.text().strip()
        confirm_password = self.confirm_password_entry.text().strip()
        
        # Validate input fields
        if not username or not email or not password or not confirm_password:
            return
        
        # Check if passwords match
        if password != confirm_password:
            return
        
        # Attempt to add the user using the User model
        result = User().add_user(username=username, email=email, password=password)
        if result:
            self.accept()  # Close the dialog with success
        else:
            self.reject()  # Close the dialog with failure
        
# Entry point for the application
if __name__ == "__main__":
    # Initialize the application
    app = QApplication(sys.argv)
    
    # Create and show the signup window
    window = Signup()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())