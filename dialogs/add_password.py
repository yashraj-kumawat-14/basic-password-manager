import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QDialog, QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QMessageBox
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from model.User import User
from model.Password import Password

class AddPassword(QDialog):
    def __init__(self, parent=None, user_id=None):
        super().__init__(parent=parent)
        self.user_id = user_id

        self.setWindowTitle("Add Password")
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        self.setGeometry(400, 300, 550, 200)

        # Username field
        self.username_label = QLabel("Username")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")

        # Password field
        self.password_label = QLabel("Password")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter a strong password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")

        # Site field
        self.sites_label = QLabel("Website URL")
        self.sites = QLineEdit()
        self.sites.setPlaceholderText("https://example.com")
        self.sites.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")

        # Note field
        self.note_label = QLabel("Note")
        self.note = QLineEdit()
        self.note.setPlaceholderText("Add additional details (optional)")
        self.note.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")

        # Grid Layout
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username, 0, 1)

        grid_layout.addWidget(self.sites_label, 0, 2)
        grid_layout.addWidget(self.sites, 0, 3)

        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password, 1, 1)

        grid_layout.addWidget(self.note_label, 1, 2)
        grid_layout.addWidget(self.note, 1, 3)

        main_layout.addLayout(grid_layout)

        # Button layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        # Apply styles
        common_css = '''
            QPushButton {
                border: 1px solid black;
                border-radius: 10px;
                padding: 5px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #F9FAFB;
            }
            QPushButton:pressed {
                background-color: #F0F0F0;
            }
        '''

        for btn in [self.save_button, self.cancel_button]:
            btn.setStyleSheet(common_css)

        # Add buttons to layout
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Connect buttons
        self.cancel_button.clicked.connect(self.reject)

        self.save_button.clicked.connect(self.save_password)

    def save_password(self):
        username = self.username.text()
        password = self.password.text()
        site = self.sites.text()
        note = self.note.text()
        
        user_model = User()
        master_username = user_model.check_user_exists_by_id(user_id=self.user_id)
        if(not username or not site):
            QMessageBox.critical(self, "Error", "Username and Website URL cannot be empty.")
            return
        elif not master_username:
            QMessageBox.critical(self, "Error", "User doesn't exists.")
            return
        print("saving password...")
        try:
            password_model = Password()
            password_model.add_password(user_id=self.user_id, username=username, password=password, site_name=site, note=note)
            print("password saved")
            self.accept()
        except Exception as e:
            print("Error occured", e)
            QMessageBox.critical(self, "Error", "Password wasn't added.")
            self.reject()
            

      




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddPassword()
    window.resize(650, 250)
    window.show()
    sys.exit(app.exec())
