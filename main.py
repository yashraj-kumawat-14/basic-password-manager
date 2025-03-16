# Main entry point of the application #


# Importing necessary modules and libraries

from PySide6.QtWidgets import QWidget, QApplication, QDialog
from dialogs.login import Login
import sys


# Main class which displays the main entry window of application to user
class Main(QWidget):
    def __init__(self, username=None):
        # Initiation QWidget class
        super().__init__()
        
        # Setting the title
        self.setWindowTitle("Basic Password Manager")
        
        # Initiating username
        self.username = username
    

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
    
    # Getting username
    username = authenticate()
    
    # Exit if no valid user
    if not username:
        print("closing")
        sys.exit(0)
    
    # Creating application's entry point
    window = Main(username)
    window.show()
    
    # Starting the eventloop
    sys.exit(app.exec())