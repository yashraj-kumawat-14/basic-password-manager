import os
import sqlite3
from dotenv import load_dotenv
import sys
from cryptography.fernet import Fernet

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__+"/..")), "database"))
print(os.path.join(os.path.dirname(os.path.abspath(__file__+"/..")), "database"))
sys.path.append(os.path.dirname(__file__))
# Load environment variables from .env file
load_dotenv()


class User:
    def __init__(self):
        self.key=None
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

    def create_connection(self):
        """Establish a connection to the database."""
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

        # Check if .env file exists
        if not os.path.exists(env_path):
            print("Generating new .env file... and encryption key")
            key = Fernet.generate_key().decode()

            from create_env import create_env_file
            create_env_file()

            # Reload environment variables
            load_dotenv()

        key = os.getenv("SECRET_KEY")
        if not key:
            raise ValueError("SECRET_KEY is missing from the environment variables.")

        self.cipher = Fernet(key.encode())
        print(self.cipher, "cipher")

        DB_NAME = os.getenv("DB_NAME", "password_manager.db")  # Default database name

        # Absolute path to the database
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", DB_NAME))
        print("db_path:", db_path)

        # Check if the database file exists
        if not os.path.exists(db_path):
            import schema  # Ensure `schema.py` creates the required database
            print("Database does not exist. Creating one.")

        return sqlite3.connect(db_path)

    def add_user(self, username, email, password):
        """Insert a new user into the database."""
        try:
            query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
            self.cursor.execute(query, (username, email, password))
            self.conn.commit()
            return True
        except:
            return False

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
    
    def check_user_exists_by_id(self, user_id):
        """Check if a user exits with the given username and password"""
        query = "SELECT username FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        data = self.cursor.fetchone()
        if data:
            return data[0] 
        return None

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
