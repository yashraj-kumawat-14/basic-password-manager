from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QApplication, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from model.User import User
from model.Password import Password
from dialogs.signup import Signup
from dialogs.forgot_password import ForgotPassword

# Login class for displaying login window and handling the logic of login
class Login(QDialog):
    def __init__(self, parent=None):
        # Initiation QDialog class
        super().__init__(parent)
        
        self.setGeometry(100, 100, 420, 250)
        
        # Initialising self.user_id to None
        self.user_id = None
        
        # Setting title to 'Login'
        self.setWindowTitle("Login")
        
        # Creating Layouts
        layout = QGridLayout()
        
        # Creating message label for displaying messages of error, success
        self.message_label = QLabel("Enter Your credentials")
        
        username_label = QLabel("Username or Email:")
        password_label = QLabel("Password:")
        
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.checkCredentials)

        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.show_signup_form)
        
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
    
    def show_signup_form(self):
        print('signup form')
        Signup(self).exec()
        
    
    def forgot_password(self):
        print("show forgot password window")
        ForgotPassword(self).exec()


    def checkCredentials(self):
        identifier = self.username_entry.text()
        password = self.password_entry.text()
        user_id = User().get_user_by_email(email=identifier, password=password)
        
        if not user_id:
            user_id = User().get_user_by_username(username=identifier, password=password)
        
        if user_id:
            print("user exists")
            self.user_id = user_id
            print(user_id, "user id is left")
            self.accept()
        else:
            print("user doesn't exist")
            QMessageBox.critical(self, "Login Failed", "Invalid username or password. Please try again.")

        

if __name__ == "__main__":
    # Starting our login application #
    
    # Initiating eventloop
    app = QApplication(sys.argv)
    
    # Creating login window
    window = Login()
    window.show()
    
    # Starting the eventloop
    sys.exit(app.exec())
