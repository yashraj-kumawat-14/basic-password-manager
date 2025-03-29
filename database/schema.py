"""
Script to define and create the database schema for the password manager.
"""

import sqlite3  # SQLite library for database operations

# Connect to the SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("password_manager.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Enable foreign key constraints for the database
cursor.execute("PRAGMA foreign_keys = ON;")

# Drop tables if they exist (for a fresh setup)
# This ensures that the script can be run multiple times without errors
cursor.execute("DROP TABLE IF EXISTS passwords;")
cursor.execute("DROP TABLE IF EXISTS users;")

# Commit the changes to the database
conn.commit()

# Create the `passwords` table
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each password
    user_id INT NOT NULL,                  -- Foreign key referencing the user
    site_name TEXT NOT NULL,               -- Name of the website or application
    username TEXT NOT NULL,                -- Username for the account
    password TEXT NOT NULL,                -- Encrypted password
    note TEXT DEFAULT '',                  -- Optional note for additional details
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE  -- Cascade delete
)
'''
)

# Create the `users` table
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each user
    username TEXT NOT NULL UNIQUE,         -- Unique username for the user
    password TEXT NOT NULL,                -- Encrypted password for the user
    email TEXT NOT NULL UNIQUE             -- Unique email address for the user
)
'''
)

# Commit the changes to the database
conn.commit()


# Commit any remaining changes (if any)
conn.commit()