"""
Dialog to add a new password to the password manager.
"""

# Import necessary modules and libraries
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QDialog, QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QMessageBox
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Import models for user and password operations
from model.User import User
from model.Password import Password

class AddPassword(QDialog):
    """
    Dialog class for adding a new password.
    """
    def __init__(self, parent=None, user_id=None):
        # Initialize the QDialog class
        super().__init__(parent=parent)
        self.user_id = user_id  # Store the authenticated user's ID

        # Set the dialog title and geometry
        self.setWindowTitle("Add Password")
        self.setGeometry(400, 300, 550, 200)

        # Create the main layout and grid layout
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Username field
        self.username_label = QLabel("Username")  # Label for the username field
        self.username = QLineEdit()  # Input field for the username
        self.username.setPlaceholderText("Enter your username")  # Placeholder text
        self.username.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")  # Styling

        # Password field
        self.password_label = QLabel("Password")  # Label for the password field
        self.password = QLineEdit()  # Input field for the password
        self.password.setPlaceholderText("Enter a strong password")  # Placeholder text
        self.password.setEchoMode(QLineEdit.EchoMode.Password)  # Hide the password input
        self.password.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")  # Styling

        # Site field
        self.sites_label = QLabel("Website URL")  # Label for the website field
        self.sites = QLineEdit()  # Input field for the website
        self.sites.setPlaceholderText("https://example.com")  # Placeholder text
        self.sites.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")  # Styling

        # Note field
        self.note_label = QLabel("Note")  # Label for the note field
        self.note = QLineEdit()  # Input field for additional notes
        self.note.setPlaceholderText("Add additional details (optional)")  # Placeholder text
        self.note.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")  # Styling

        # Add fields to the grid layout
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username, 0, 1)
        grid_layout.addWidget(self.sites_label, 0, 2)
        grid_layout.addWidget(self.sites, 0, 3)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password, 1, 1)
        grid_layout.addWidget(self.note_label, 1, 2)
        grid_layout.addWidget(self.note, 1, 3)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Button layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")  # Save button
        self.cancel_button = QPushButton("Cancel")  # Cancel button

        # Apply styles to buttons
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

        # Add buttons to the button layout
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Set the main layout for the dialog
        self.setLayout(main_layout)

        # Connect button signals to their respective slots
        self.cancel_button.clicked.connect(self.reject)  # Close the dialog on cancel
        self.save_button.clicked.connect(self.save_password)  # Save the password on save

    def save_password(self):
        """
        Saves the entered password to the database.
        """
        # Get input values
        username = self.username.text()
        password = self.password.text()
        site = self.sites.text()
        note = self.note.text()
        
        # Check if the user exists
        user_model = User()
        master_username = user_model.check_user_exists_by_id(user_id=self.user_id)
        
        # Validate input fields
        if not username or not site:
            QMessageBox.critical(self, "Error", "Username and Website URL cannot be empty.")
            return
        elif not master_username:
            QMessageBox.critical(self, "Error", "User doesn't exist.")
            return
        
        try:
            # Save the password using the Password model
            password_model = Password()
            password_model.add_password(user_id=self.user_id, username=username, password=password, site_name=site, note=note)
            self.accept()  # Close the dialog with success
        except Exception as e:
            QMessageBox.critical(self, "Error", "Password wasn't added.")  # Show error message
            self.reject()  # Close the dialog with failure


if __name__ == "__main__":
    # Entry point for testing the dialog
    app = QApplication(sys.argv)
    window = AddPassword()
    window.resize(650, 250)
    window.show()
    sys.exit(app.exec())