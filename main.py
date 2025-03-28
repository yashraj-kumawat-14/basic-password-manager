"""
Basic Password Manager
Main entry point of the application.
"""

import sys
from PySide6.QtWidgets import (
    QWidget, QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QHeaderView, QSizePolicy, QTreeWidgetItem,
    QPushButton
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from get_favicon import get_favicon
from dialogs.login import Login
from dialogs.add_password import AddPassword
from dialogs.view_password import ViewPassword
from model.Password import Password
import os


class Main(QWidget):
    """
    Main application window for the password manager.
    """
    def __init__(self, user_id = None):
        super().__init__()
        self.setWindowTitle("Basic Password Manager")
        self.user_id = user_id

        # Create UI elements
        self.init_ui()
        
        # Load passwords into the list
        self.load_user_passwords()

    def init_ui(self):
        """
        Initializes the user interface.
        """
        main_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        
        passwords_label = QLabel("Passwords")
        passwords_label.setStyleSheet("font-size:25px; font-weight: bold; font-family: Arial;")
        
        add_password_button = QPushButton("  Add")
        add_password_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        add_password_button.clicked.connect(self.add_password)
        
        add_password_button.setStyleSheet("background-color: #90EE90;")
        add_password_button.setIcon(QIcon("./images/add.png"))
        
        h_layout.addWidget(passwords_label)
        h_layout.addWidget(add_password_button)
        
        # Information label
        information_label = QLabel("Create, save, and manage your passwords so you can easily sign in to sites and apps.")
        information_label.setStyleSheet("font-size:15px; font-family: Arial;")
        
        # Password list
        self.password_list = QTreeWidget(self)
        self.password_list.setHeaderLabels(["S.no.", "Site Name", "Action"])
        self.password_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.password_list.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_list.setHeaderHidden(True)

        
        # Set column resize policies
        self.password_list.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.password_list.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.password_list.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        # Add widgets to layout
        main_layout.addLayout(h_layout)
        main_layout.addWidget(information_label)
        main_layout.addWidget(self.password_list)
        
        self.setLayout(main_layout)

    def add_password(self):
        print("adding password")
        add_password = AddPassword(parent=self)
        result = add_password.exec()
        print(result)
        if result == QDialog.Accepted:
            print("New password added")
            self.refresh()
            return
        
    def load_user_passwords(self):
        """
        Loads the user's saved passwords into the QTreeWidget.
        """
        # data = [
        #     ("1", "yahoo.com", "12345"),
        #     ("2", "chatgpt.com", "4567"),
        #     ("3", "google.com", "234324")
        # ]
        


        data = Password().get_password_by_user_id(user_id=self.user_id)
        print(data, "data")
        self.password_list.clear()
        count = 1
        for item in data:
            print(item)
            row = QTreeWidgetItem(self.password_list, [str(count)])
            
            for i in range(row.columnCount()):
                row.setTextAlignment(i, Qt.AlignmentFlag.AlignCenter)
                
            # Create widget for site name (icon + label)
            site_name_widget = QWidget()
            layout = QHBoxLayout(site_name_widget)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            icon = QLabel()
            self.set_icon(icon_widget=icon, name=item[2])
            icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            label = QLabel(item[2])
            
            layout.addWidget(icon)
            layout.addWidget(label)
            
            # Create a widget to hold the button
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            # button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for better fitting
                
            button = QPushButton("View")
            button.setFixedSize(90, 25)  # Adjust button size if needed
            button.clicked.connect(lambda _, password_id=item[0]: self.view_password(password_id))
                
            # Add button to layout and set layout to widget
            button_layout.addWidget(button)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_widget.setLayout(button_layout)
            
            self.password_list.setItemWidget(row, 1, site_name_widget)
            self.password_list.setItemWidget(row, 2, button_widget)
            count+=1
    
    def set_icon(self, icon_widget, name):
        file_path = f"./images/icons/{name}.png"
        if os.path.exists(file_path):
            print("Icon already exists for", name)
            icon_widget.setPixmap(QPixmap(file_path).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            return None
        
        save_path = get_favicon(name, name)
        if(save_path):
            icon_widget.setPixmap(QPixmap(save_path).scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            return None
        
        icon_widget.setPixmap(QPixmap("./images/icons/default.png").scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def view_password(self, password_id):
        ViewPassword(parent=self,password_id=password_id).exec()

    def refresh(self):
        self.load_user_passwords()

def authenticate():
    """
    Handles user authentication.
    """
    login = Login()
    result = login.exec()
    if result == QDialog.Accepted:
        print("Logged in")
        return login.user_id
    return None


if __name__ == "__main__":
    # Initialize application
    app = QApplication(sys.argv)
    
    # Authenticate user (commented out for testing)
    user_id = authenticate()
    if not user_id:
        print("Closing application")
        sys.exit(0)
    
    # Launch main window
    window = Main(user_id=user_id)
    window.show()
    
    sys.exit(app.exec())