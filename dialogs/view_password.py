import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDialog,QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout
from PySide6.QtGui import QIcon

class ViewPassword(QDialog):
    def __init__(self, parent=None, user_id = None):
        super().__init__(parent=parent)
        self.user_id = user_id

        self.setWindowTitle("Add Password")
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Username field
        self.username_label = QLabel("Username")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")
        self.copy_username = QPushButton(QIcon("./images/copy_icon.png"), "")

        # Password field
        self.password_label = QLabel("Password")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Secure your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("background-color: #e0e0e0; border-radius: 5px; padding: 5px;")
        self.show_password = QPushButton(QIcon("./images/eye_icon.png"), "")

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
        grid_layout.addWidget(self.copy_username, 0, 2)

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
        self.share_button = QPushButton("Share")

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        # Initially hide Save & Cancel buttons
        self.save_button.hide()
        self.cancel_button.hide()

        # Apply styles
        common_css = '''
            QPushButton {
                border: 1px solid black;
                border-radius: 10px;
                padding: 5px;
                background-color: white;
                transition: background-color 0.2s ease-in-out;
            }
            QPushButton:hover {
                background-color: #F9FAFB;
            }
            QPushButton:pressed {
                background-color: #F0F0F0;
            }
        '''
        
        for btn in [self.share_button, self.edit_button, self.delete_button, self.save_button, self.cancel_button]:
            btn.setStyleSheet(common_css)

        # Add buttons to layout
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.share_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Connect buttons
        self.edit_button.clicked.connect(self.enable_editing)
        self.cancel_button.clicked.connect(self.disable_editing)

    def enable_editing(self):
        """Enable editing and show Save & Cancel buttons."""
        self.sites.setReadOnly(False)
        self.note.setReadOnly(False)
        
        self.save_button.show()
        self.cancel_button.show()
        self.edit_button.hide()

    def disable_editing(self):
        """Disable editing and hide Save & Cancel buttons."""
        self.sites.setReadOnly(True)
        self.note.setReadOnly(True)

        self.save_button.hide()
        self.cancel_button.hide()
        self.edit_button.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewPassword()
    window.resize(650, 250)
    window.show()
    sys.exit(app.exec())