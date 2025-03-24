import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Password:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

    def create_connection(self):
        """Establish a connection to the database."""
        DB_NAME = os.getenv("DB_NAME", "password_manager.db")  # Default to 'password_manager.db' if not set
        return sqlite3.connect(DB_NAME)

    def add_password(self, site_name, username, password):
        """Insert a new password record into the database."""
        query = "INSERT INTO passwords (site_name, username, password) VALUES (?, ?, ?)"
        self.cursor.execute(query, (site_name, username, password))
        self.conn.commit()

    def update_password(self, password_id, new_password):
        """Update a stored password by ID."""
        query = "UPDATE passwords SET password = ? WHERE id = ?"
        self.cursor.execute(query, (new_password, password_id))
        self.conn.commit()

    def delete_password(self, password_id):
        """Delete a password record by ID."""
        query = "DELETE FROM passwords WHERE id = ?"
        self.cursor.execute(query, (password_id,))
        self.conn.commit()

    def get_all_passwords(self):
        """Retrieve all stored passwords."""
        query = "SELECT * FROM passwords"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_password_by_id(self, password_id):
        """Retrieve a specific password by ID."""
        query = "SELECT * FROM passwords WHERE id = ?"
        self.cursor.execute(query, (password_id,))
        return self.cursor.fetchone()
    
    def get_password_by_user_id(self, user_id):
        """Retrieve all password associated with user id."""
        query = "SELECT * FROM passwords WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def get_password_by_username(self, username):
        """Retrieve all password associated with username."""
        query = "SELECT * FROM passwords WHERE username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchall()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()

