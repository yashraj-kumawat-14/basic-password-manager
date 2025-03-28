import os
import sqlite3
from dotenv import load_dotenv
import sys
from cryptography.fernet import Fernet

# Ensure the correct path for database module import
sys.path.append(os.path.join(os.path.dirname(__file__), "database"))
sys.path.append(os.path.dirname(__file__))
print(os.path.join(os.path.dirname(__file__), "database"))

# Load environment variables from .env file
load_dotenv()


class Password:
    def __init__(self):
        self.cipher = None
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

    def add_password(self, user_id, site_name, username, password, note):
        """Insert a new password record into the database, including a note."""
        print(site_name, username, password, note)
        query = "INSERT INTO passwords (user_id, site_name, username, password, note) VALUES (?, ?, ?, ?, ?)"
        encrypted_password = self.cipher.encrypt(password.encode())
        self.cursor.execute(query, (user_id, site_name, username, encrypted_password.decode(), note))
        self.conn.commit()

    def update_password(self, password_id, new_username, new_password, new_site, new_note):
        """Update all fields of a stored password by ID."""
        query = "UPDATE passwords SET username = ?, password = ?, site_name = ?, note = ? WHERE id = ?"
        try:
            encrypted_password = self.cipher.encrypt(new_password.encode())
            self.cursor.execute(query, (new_username, encrypted_password.decode(), new_site, new_note, password_id))
            self.conn.commit()
            return True
        except Exception as e:
            print("Database Error:", e)
            return False

    def delete_password(self, password_id):
        """Delete a password record by ID."""
        query = "DELETE FROM passwords WHERE id = ?"
        self.cursor.execute(query, (password_id,))
        self.conn.commit()

    def get_all_passwords(self):
        print("getting all passwords")
        """Retrieve all stored passwords with decrypted entries."""
        query = "SELECT * FROM passwords"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        print(records, "records")

        decrypted_records = []
        for record in records:
            decrypted_password = self.cipher.decrypt(record[4]).decode()
            decrypted_records.append(record[:4] + (decrypted_password,) + record[5:])

        return decrypted_records

    def get_password_by_id(self, password_id):
        """Retrieve a specific password by ID."""
        query = "SELECT * FROM passwords WHERE id = ?"
        self.cursor.execute(query, (password_id,))
        password = self.cursor.fetchone()
        if password:
            decrypted_password = self.cipher.decrypt(password[4]).decode()
            return password[:4] + (decrypted_password,) + password[5:]
        return None

    def get_password_by_user_id(self, user_id):
        """Retrieve all passwords associated with user ID."""
        query = "SELECT * FROM passwords WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        records = self.cursor.fetchall()

        decrypted_records = []
        for record in records:
            decrypted_password = self.cipher.decrypt(record[4]).decode()
            decrypted_records.append(record[:4] + (decrypted_password,) + record[5:])

        return decrypted_records

    def get_password_by_username(self, username):
        """Retrieve all passwords associated with a username."""
        query = "SELECT * FROM passwords WHERE username = ?"
        self.cursor.execute(query, (username,))  # Fixed missing execution
        records = self.cursor.fetchall()

        decrypted_records = []
        for record in records:
            decrypted_password = self.cipher.decrypt(record[4]).decode()
            decrypted_records.append(record[:4] + (decrypted_password,) + record[5:])

        return decrypted_records

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
