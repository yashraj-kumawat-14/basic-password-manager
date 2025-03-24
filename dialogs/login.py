# Login Dialog to display login window to user #


# Importing necessary modules and libraries

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QApplication, QGridLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from model.User import User


# Login class for displaying login window and handling the logic of login
class Login(QDialog):
    def __init__(self, parent=None):
        # Initiation QDialog class
        super().__init__(parent)
        
        self.setGeometry(100, 100, 350, 250)
        
        # Initialising self.username to None
        self.username = None
        
        # Setting title to 'Login'
        self.setWindowTitle("Login")
        
        # Creating Layouts
        layout = QGridLayout()
        
        # Creating message label for displaying messages of error, success
        self.message_label = QLabel("Enter Your credentials")
        
        username_label = QLabel("Username :")
        password_label = QLabel("Password :")
        
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.checkCredentials)

        signup_button = QPushButton("Sign Up")
        
        forgot_password_link = QLabel('<a href="#">Forgot Password?</a>')
        forgot_password_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forgot_password_link.setOpenExternalLinks(False)  # Prevent opening a browser
        forgot_password_link.linkActivated.connect(self.forgot_password)
        
        
        self.message_label.setStyleSheet("color: Black; font-size: 19px; padding:10px")
        
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        password_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout.addWidget(self.message_label, 0, 0, 1, 3)
        layout.addWidget(username_label, 1, 0, 1, 1)
        layout.addWidget(self.username_entry, 1, 1, 1, 2)
        layout.addWidget(password_label, 2, 0, 1, 1)
        layout.addWidget(self.password_entry, 2, 1, 1, 2)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 3, 0, 1, 3)
        layout.addWidget(login_button, 4, 1, 1, 1)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 5, 0, 1, 3)
        layout.addWidget(forgot_password_link, 6, 0, 1, 3)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 7, 0, 1, 3)
        layout.addWidget(signup_button, 8, 1, 1, 1)
        
        self.setLayout(layout)
    
    def forgot_password(self):
        print("show forgot password window")
    
    def checkCredentials(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        user_id = User().check_user_exists(username=username, password=password)
        if(user_id):
            print("user exists")
            self.accept()
        else:
            print("user don't exists")
            self.reject()
        

if __name__ == "__main__":
    # Starting our login application #
    
    # Initiating eventloop
    app = QApplication(sys.argv)
    
    # Creating login window
    window = Login()
    window.show()
    
    # Starting the eventloop
    sys.exit(app.exec())