"""
User model to handle user-related operations in the database.
"""

import os
import sqlite3
from dotenv import load_dotenv
import sys
from cryptography.fernet import Fernet

# Add the database directory to the system path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__ + "/..")), "database"))
sys.path.append(os.path.dirname(__file__))

# Load environment variables from the .env file
load_dotenv()


class User:
    """
    User model class to interact with the users table in the database.
    """
    def __init__(self):
        self.key = None  # Encryption key
        self.conn = self.create_connection()  # Establish a database connection
        self.cursor = self.conn.cursor()  # Create a cursor for executing queries

    def create_connection(self):
        """
        Creates a connection to the SQLite database.
        """
        # Retrieve the encryption key from environment variables
        key = os.getenv("SECRET_KEY")
        if not key:
            raise ValueError("SECRET_KEY is missing from the environment variables.")

        # Initialize the encryption cipher
        self.cipher = Fernet(key.encode())

        # Get the database name from environment variables or use the default
        DB_NAME = os.getenv("DB_NAME", "password_manager.db")

        # Absolute path to the database
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", DB_NAME))

        # Check if the database file exists
        if not os.path.exists(db_path):
            import schema  # Ensure `schema.py` creates the required database

        return sqlite3.connect(db_path)

    def add_user(self, username, email, password):
        """
        Insert a new user into the database.
        """
        try:
            query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
            self.cursor.execute(query, (username, email, password))
            self.conn.commit()
            return True
        except:
            return False

    def update_user_password(self, user_id, new_password):
        """
        Update a user's password by ID.
        """
        query = "UPDATE users SET password = ? WHERE id = ?"
        self.cursor.execute(query, (new_password, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        """
        Delete a user by ID.
        """
        query = "DELETE FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def get_all_users(self):
        """
        Retrieve all users from the database.
        """
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_by_id(self, user_id):
        """
        Retrieve a specific user by ID.
        """
        query = "SELECT * FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def get_user_by_username(self, username):
        """
        Retrieve a specific user by username.
        """
        query = "SELECT * FROM users WHERE id = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()
    
    def check_user_exists(self, username, password):
        """
        Check if a user exists with the given username and password.
        """
        query = "SELECT id FROM users WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        data = self.cursor.fetchone()
        if data:
            return data[0] 
        return None
    
    def get_user_by_email(self, email, password):
        """
        Check if a user exists with the given email and password.
        """
        query = "SELECT id FROM users WHERE email = ? AND password = ?"
        self.cursor.execute(query, (email, password))
        data = self.cursor.fetchone()
        if data:
            return data[0] 
        return None
    
    def get_user_by_username(self, username, password):
        """
        Check if a user exists with the given username and password.
        """
        query = "SELECT id FROM users WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        data = self.cursor.fetchone()
        if data:
            return data[0] 
        return None
    
    def check_user_exists_by_email(self, email):
        """
        Check if a user exists with the given email.
        """
        query = "SELECT id FROM users WHERE email = ?"
        self.cursor.execute(query, (email,))
        data = self.cursor.fetchone()
        if data:
            return data[0] 
        return None
    
    def check_user_exists_by_id(self, user_id):
        """
        Check if a user exists with the given user ID.
        """
        query = "SELECT username FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        data = self.cursor.fetchone()
        if data:
            return data[0] 
        return None

    def close_connection(self):
        """
        Close the database connection.
        """
        self.conn.close()