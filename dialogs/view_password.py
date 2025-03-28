
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QDialog,QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QMessageBox)

from PySide6.QtGui import QIcon
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from model.User import User
from model.Password import Password

class ViewPassword(QDialog):
    def __init__(self, parent=None, password_id = None):
        self.parent = parent
        super().__init__(parent=parent)
        self.password_id = password_id

        self.setWindowTitle("View Password")
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Username field  
        self.username_label = QLabel("Username")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")
        self.copy_password = QPushButton(QIcon("./images/copy_icon.png"), "")
        self.copy_password.setToolTip("Copy Password")
        self.copy_password.clicked.connect(self.copy_to_clipboard) 
        self.username.setReadOnly(True)

        # Password field
        self.password_label = QLabel("Password")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Secure your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")
        self.show_password = QPushButton(QIcon("./images/eye_icon.png"), "")
        self.show_password.setCheckable(True)
        self.show_password.clicked.connect(self.toggle_password_visibility)
        self.password.setReadOnly(True)

        # Site field
        self.sites_label = QLabel("Website URL")
        self.sites = QLineEdit()
        self.sites.setPlaceholderText("https://example.com")
        self.sites.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")
        self.sites.setReadOnly(True)
        

        # Note field
        self.note_label = QLabel("Note")
        self.note = QLineEdit()
        self.note.setPlaceholderText("Add additional details (optional)")
        self.note.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")
        self.note.setReadOnly(True)

        # Grid Layout
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username, 0, 1)
        grid_layout.addWidget(self.copy_password, 0, 2)

        grid_layout.addWidget(self.sites_label, 0, 3)
        grid_layout.addWidget(self.sites, 0, 4)

        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password, 1, 1)
        grid_layout.addWidget(self.show_password, 1, 2)

        grid_layout.addWidget(self.note_label, 1, 3)
        grid_layout.addWidget(self.note, 1, 4)

        main_layout.addLayout(grid_layout)

        # Button layout
        button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_password)
        # self.share_button = QPushButton("Share")

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        
        self.save_button.clicked.connect(self.update_password)

        # Initially hide Save & Cancel buttons
        self.save_button.hide()
        self.cancel_button.hide()
        
        # Apply styles
        self.edit_button.setStyleSheet("""
        QPushButton {
            background-color: #007BFF; /* Blue */
            color: white;
            border-radius: 8px;
            padding: 8px 12px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
    """)

        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545; /* Red */
                color: white;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #A71D2A;
            }
        """)

        # self.share_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #28A745; /* Green */
        #         color: white;
        #         border-radius: 8px;
        #         padding: 8px 12px;
        #     }
        #     QPushButton:hover {
        #         background-color: #1E7E34;
        #     }
        # """)

        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745; /* Green */
                color: white;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #1E7E34;
            }
        """)

        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6C757D; /* Gray */
                color: white;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #545B62;
            }
        """)

        
        # Add buttons to layout
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        # button_layout.addWidget(self.share_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Connect buttons
        self.edit_button.clicked.connect(self.enable_editing)
        self.cancel_button.clicked.connect(self.disable_editing)
        
        self.load_password()

    def toggle_password_visibility(self, value):
        print(value)
        self.password.setEchoMode(QLineEdit.EchoMode.Normal) if value else self.password.setEchoMode(QLineEdit.EchoMode.Password) 
    
    def update_password(self):
        """Update all fields of the password entry in the database."""
        updated_username = self.username.text().strip()
        updated_password = self.password.text().strip()
        updated_site = self.sites.text().strip()
        updated_note = self.note.text().strip()

        if not updated_username or not updated_password or not updated_site:
            print("Error: Username, password, and site cannot be empty!")
            return

        success = Password().update_password(
            password_id=self.password_id,
            new_username=updated_username,
            new_password=updated_password,
            new_site=updated_site,
            new_note=updated_note
        )

        if success:
            print("Password updated successfully!")
            self.disable_editing()
        else:
            print("Failed to update password.")


    
    def enable_editing(self):
        """Enable editing and show Save & Cancel buttons."""
        self.sites.setReadOnly(False)
        self.note.setReadOnly(False)
        self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        self.username.setReadOnly(False)
        self.password.setReadOnly(False)
        
        self.save_button.show()
        self.cancel_button.show()
        self.edit_button.hide()

    def disable_editing(self):
        """Disable editing and hide Save & Cancel buttons."""
        self.sites.setReadOnly(True)
        self.note.setReadOnly(True)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.username.setReadOnly(True)
        self.password.setReadOnly(True)

        self.save_button.hide()
        self.cancel_button.hide()
        self.edit_button.show()
        
    def load_password(self):
        passwordData = Password().get_password_by_id(password_id=self.password_id)
        print("hellO", passwordData)
        if passwordData:
            site_name = passwordData[2]
            username = passwordData[3]
            password = passwordData[4]
            note = "tayt"#passwordData[5]
            
            self.username.setText(username)
            self.password.setText(password)
            self.sites.setText(site_name)
            self.note.setText(note)
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()  # Get clipboard instance
        clipboard.setText(self.password.text())  # Copy QLineEdit text
        
    def delete_password(self):
        result = QMessageBox.question(self, "Are you sure ?", "Are you sure about deleting this password ?")
        
        if result == QMessageBox.Yes:
            print("yes")
            Password().delete_password(password_id=self.password_id)
            print("Password deleted successfully.")
            if self.parent:
                self.parent.refresh()
            self.reject()
        else:
            print("no")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewPassword(password_id=1)
    window.resize(650, 250)
    window.show()
    sys.exit(app.exec())