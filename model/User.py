import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class User:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

    def create_connection(self):
        """Establish a connection to the database."""
        DB_NAME = os.getenv("DB_NAME", "password_manager.db")  # Default to 'password_manager.db' if not set
        return sqlite3.connect(DB_NAME)

    def add_user(self, username, email, password):
        """Insert a new user into the database."""
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        self.cursor.execute(query, (username, email, password))
        self.conn.commit()

    def update_user_password(self, user_id, new_password):
        """Update a user's password by ID."""
        query = "UPDATE users SET password = ? WHERE id = ?"
        self.cursor.execute(query, (new_password, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        """Delete a user by ID."""
        query = "DELETE FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def get_all_users(self):
        """Retrieve all users."""
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_by_id(self, user_id):
        """Retrieve a specific user by ID."""
        query = "SELECT * FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def get_user_by_username(self, username):
        """Retrieve a specific user by username."""
        query = "SELECT * FROM users WHERE id = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()
    
    def check_user_exists(self, username, password):
        """Check if a user exits with the given username and password"""
        query = "SELECT id FROM users WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        data = self.cursor.fetchone()
        if data:
            return data[0] 
        return None

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
