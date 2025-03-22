# Main entry point of the application #


# Importing necessary modules and libraries

from PySide6.QtWidgets import QWidget, QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout
from dialogs.login import Login
import sys


# Main class which displays the main entry window of application to user
class Main(QWidget):
    def __init__(self, username=None):
        # Initiation QWidget class
        super().__init__()
        
        # Setting the title
        self.setWindowTitle("Basic Password Manager")
        
        # Passwords label
        passwords_label = QLabel("Passwords")
        passwords_label.setStyleSheet("font-size:25px; font-weight: bold; font-family: Arial;")
        
        # information_label
        information_label = QLabel("Create, save, and manage your passwords so you can easily sign in to sites and apps.")
        information_label.setStyleSheet("font-size:15px; font-family: Arial;")
        
        # creating main layout
        main_layout = QVBoxLayout()
        
        # Initiating username
        self.username = username
        
        main_layout.addWidget(passwords_label)
        main_layout.addWidget(information_label)
        
        # Setting applications main layout
        self.setLayout(main_layout)
    

# Function to handle the login of user and return its username if right credentials were entered by user
def authenticate():
    login = Login()
    result = login.exec()
    if  result == QDialog.Accepted:
        print("loggedin")
        return login.username
    return None        


if __name__ == "__main__":
    # Starting our application #
    
    # Initiating eventloop
    app = QApplication(sys.argv)
    
    # # Getting username
    # username = authenticate()
    
    # # Exit if no valid user
    # if not username:
    #     print("closing")
    #     sys.exit(0)
    
    # Creating application's entry point
    window = Main(username="admin")
    window.show()
    
    # Starting the eventloop
    sys.exit(app.exec())