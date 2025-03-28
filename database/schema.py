import sqlite3

conn = sqlite3.connect("password_manager.db")

cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Drop tables if they exist (for fresh setup)
cursor.execute("DROP TABLE IF EXISTS passwords;")
cursor.execute("DROP TABLE IF EXISTS users;")

conn.commit()

cursor.execute(
'''
CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    site_name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    note TEXT DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
)
'''
)


cursor.execute(
'''
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
'''
)

# Insert dummy users
cursor.execute("INSERT INTO users (username, password, email) VALUES ('admin', '1234', 'john@example.com');")
cursor.execute("INSERT INTO users (username, password, email) VALUES ('alice_wonder', 'hashed_password2', 'alice@example.com');")
cursor.execute("INSERT INTO users (username, password, email) VALUES ('dev_user', 'hashed_password3', 'dev@example.com');")

conn.commit()

# Fetch user IDs for inserting passwords
cursor.execute("SELECT id FROM users WHERE username = 'admin';")
john_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM users WHERE username = 'alice_wonder';")
alice_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM users WHERE username = 'dev_user';")
dev_id = cursor.fetchone()[0]

# Insert dummy passwords linked to users
# cursor.execute("INSERT INTO passwords (user_id, site_name, username, password) VALUES (?, 'google.com', 'john_doe', 'password123');", (john_id,))
# cursor.execute("INSERT INTO passwords (user_id, site_name, username, password) VALUES (?, 'facebook.com', 'alice_wonder', 'fb_secure_pass');", (alice_id,))
# cursor.execute("INSERT INTO passwords (user_id, site_name, username, password) VALUES (?, 'github.com', 'dev_user', 'gitpass!@#');", (dev_id,))

conn.commit()

print("Successfully created database and tables schema")

conn.commit()