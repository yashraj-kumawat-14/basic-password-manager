# Signup Dialog to display signup window to user

# Importing necessary modules and libraries

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QApplication, QGridLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from model.User import User

# Signup class for displaying signup window and handling the logic of signup
class Signup(QDialog):
    def __init__(self, parent=None):
        # Initiation QDialog class
        super().__init__(parent)
        
        self.setGeometry(100, 100, 350, 170)
        
        # Initialising self.username to None
        # self.user_id = None
        
        # Setting title to 'Signup'
        self.setWindowTitle("Signup")
        
        # Creating Layouts
        layout = QGridLayout()
        
        # Creating message label for displaying messages of error, success
        self.message_label = QLabel("Create a new account")
        
        username_label = QLabel("Username :")
        email_label = QLabel("Email :")
        password_label = QLabel("Password :")
        confirm_password_label = QLabel("Confirm Password :")
        
        self.username_entry = QLineEdit()
        self.email_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.confirm_password_entry = QLineEdit()
        
        signup_button = QPushButton("Sign Up")
        signup_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        signup_button.clicked.connect(self.registerUser)
        
        self.message_label.setStyleSheet("color: Black; font-size: 19px; padding:10px")
        
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        email_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        password_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        confirm_password_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
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
        
        self.setLayout(layout)
    
    def registerUser(self):
        username = self.username_entry.text().strip()
        email = self.email_entry.text().strip()
        password = self.password_entry.text().strip()
        confirm_password = self.confirm_password_entry.text().strip()
        
        if not username or not email or not password or not confirm_password:
            print("All fields are required")
            return
        
        if password != confirm_password:
            print("Passwords do not match")
            return
        
        result = User().add_user(username=username, email=email, password=password)
        if result:
            print("result is ", result)
            print("User registered successfully")
            self.accept()
        else:
            print("User registration failed")
            self.reject()
        
if __name__ == "__main__":
    # Starting our signup application #
    
    # Initiating eventloop
    app = QApplication(sys.argv)
    
    # Creating signup window
    window = Signup()
    window.show()
    
    # Starting the eventloop
    sys.exit(app.exec())
