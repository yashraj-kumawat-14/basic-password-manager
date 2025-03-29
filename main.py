"""
Basic Password Manager
Main entry point of the application.
"""

# Import necessary modules and libraries
import sys
from PySide6.QtWidgets import (
    QWidget, QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QHeaderView, QSizePolicy, QTreeWidgetItem,
    QPushButton
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from get_favicon import get_favicon  # Utility to fetch website favicons
from dialogs.login import Login  # Login dialog for user authentication
from dialogs.add_password import AddPassword  # Dialog to add new passwords
from dialogs.view_password import ViewPassword  # Dialog to view saved passwords
from model.Password import Password  # Model to handle password-related operations
import os


class Main(QWidget):
    """
    Main application window for the password manager.
    """
    def __init__(self, user_id=None):
        # Initialize the QWidget class
        super().__init__()
        self.setWindowTitle("Basic Password Manager")  # Set the window title
        self.user_id = user_id  # Store the authenticated user's ID

        # Create and initialize the user interface
        self.init_ui()
        
        # Load the user's saved passwords into the list
        self.load_user_passwords()

    def init_ui(self):
        """
        Initializes the user interface.
        """
        # Create the main vertical layout
        main_layout = QVBoxLayout()
        
        # Create a horizontal layout for the header
        h_layout = QHBoxLayout()
        
        # Create a label for the header
        passwords_label = QLabel("Passwords")
        passwords_label.setStyleSheet("font-size:25px; font-weight: bold; font-family: Arial;")
        
        # Create a button to add new passwords
        add_password_button = QPushButton("  Add")
        add_password_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        add_password_button.clicked.connect(self.add_password)  # Connect button to add_password method
        add_password_button.setStyleSheet("background-color: #90EE90;")  # Set button style
        add_password_button.setIcon(QIcon("./images/add.png"))  # Set button icon
        
        # Add the label and button to the horizontal layout
        h_layout.addWidget(passwords_label)
        h_layout.addWidget(add_password_button)
        
        # Create an information label
        information_label = QLabel("Create, save, and manage your passwords so you can easily sign in to sites and apps.")
        information_label.setStyleSheet("font-size:15px; font-family: Arial;")
        
        # Create a tree widget to display the list of passwords
        self.password_list = QTreeWidget(self)
        self.password_list.setHeaderLabels(["S.no.", "Site Name", "Action"])  # Set column headers
        self.password_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.password_list.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_list.setHeaderHidden(True)  # Hide the header
        
        # Set column resize policies
        self.password_list.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.password_list.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.password_list.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        # Add widgets to the main layout
        main_layout.addLayout(h_layout)
        main_layout.addWidget(information_label)
        main_layout.addWidget(self.password_list)
        
        # Set the main layout for the window
        self.setLayout(main_layout)

    def add_password(self):
        """
        Opens the AddPassword dialog to add a new password.
        """
        add_password = AddPassword(parent=self, user_id=self.user_id)  # Create the dialog
        result = add_password.exec()  # Execute the dialog
        if result == QDialog.Accepted:  # Check if the dialog was accepted
            self.refresh()  # Refresh the password list
            return
        
    def load_user_passwords(self):
        """
        Loads the user's saved passwords into the QTreeWidget.
        """
        # Fetch passwords from the database using the Password model
        data = Password().get_password_by_user_id(user_id=self.user_id)
        self.password_list.clear()  # Clear the existing list
        count = 1  # Initialize the serial number
        for item in data:
            row = QTreeWidgetItem(self.password_list, [str(count)])  # Create a new row
            
            # Align text in all columns to the center
            for i in range(row.columnCount()):
                row.setTextAlignment(i, Qt.AlignmentFlag.AlignCenter)
                
            # Create a widget for the site name (icon + label)
            site_name_widget = QWidget()
            layout = QHBoxLayout(site_name_widget)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Add an icon for the site
            icon = QLabel()
            self.set_icon(icon_widget=icon, name=item[2])
            icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            # Add a label for the site name
            label = QLabel(item[2])
            
            layout.addWidget(icon)
            layout.addWidget(label)
            
            # Create a widget to hold the "View" button
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
                
            # Create the "View" button
            button = QPushButton("View")
            button.setFixedSize(90, 25)  # Set button size
            button.clicked.connect(lambda _, password_id=item[0]: self.view_password(password_id))  # Connect button to view_password method
                
            # Add the button to the layout and set the layout to the widget
            button_layout.addWidget(button)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_widget.setLayout(button_layout)
            
            # Add the widgets to the respective columns
            self.password_list.setItemWidget(row, 1, site_name_widget)
            self.password_list.setItemWidget(row, 2, button_widget)
            count += 1  # Increment the serial number
    
    def set_icon(self, icon_widget, name):
        """
        Sets the icon for a site based on its name.
        """
        file_path = f"./images/icons/{name}.png"  # Path to the icon file
        if os.path.exists(file_path):  # Check if the icon already exists
            icon_widget.setPixmap(QPixmap(file_path).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            return None
        
        # Fetch and save the favicon if it doesn't exist
        save_path = get_favicon(name, name)
        if save_path:
            icon_widget.setPixmap(QPixmap(save_path).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            return None
        
        # Set a default icon if no favicon is found
        icon_widget.setPixmap(QPixmap("./images/icons/default.png").scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def view_password(self, password_id):
        """
        Opens the ViewPassword dialog to view a saved password.
        """
        ViewPassword(parent=self, password_id=password_id).exec()

    def refresh(self):
        """
        Refreshes the password list by reloading the user's passwords.
        """
        self.load_user_passwords()

def authenticate():
    """
    Handles user authentication.
    """
    login = Login()  # Create the login dialog
    result = login.exec()  # Execute the dialog
    if result == QDialog.Accepted:  # Check if the dialog was accepted
        return login.user_id  # Return the authenticated user's ID
    return None  # Return None if authentication failed


if __name__ == "__main__":
    # Initialize the application
    app = QApplication(sys.argv)
    
    # Authenticate the user
    user_id = authenticate()
    if not user_id:  # Exit if authentication failed
        sys.exit(0)
        
    
    # Launch the main application window
    window = Main(user_id=user_id)
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())