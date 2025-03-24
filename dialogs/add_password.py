from PySide6.QtWidgets import QDialog

class AddPassword(QDialog):
    def __init__(self, parent=None, username=None):
        super().__init__(parent=parent)
        
        self.username = username
        
        self.setWindowTitle("Add Password")
        
        
        