from cryptography.fernet import Fernet

# key = Fernet.generate_key()
key = "kDZQNSIyqxv4Ye-06zyTr2jcMscxzUDnMrKTtSNCE2E=".encode()

# with open(".env", "a") as file:
#     file.write(f"SECRET_KEY={key}") 

# # save ket to file

cipher = Fernet(key)

# message = "Hello, World!".encode()  # Convert string to bytes
# encrypted_message = cipher.encrypt(message)

# print("Encrypted Message:", encrypted_message)


# decrypted_message = cipher.decrypt(encrypted_message)
# print("Decrypted Message:", decrypted_message.decode())  # Convert bytes to string


# from dotenv import load_dotenv

# load_dotenv()
# import os 

# print(os.getenv("SECRET_KEY"))

import sqlite3

conn= sqlite3.connect("password_manager.db")
cursor = conn.cursor()
cursor.execute("Select * from passwords")
# print(cursor.fetchall())
l = cursor.fetchall()
print(l)
# print(l[0][4])
# a = cipher.decrypt('gAAAAABn5vrSfkQjq4p4X6hfhtsTLMgUQ7kf6QOe-styk_rcj-cHZDeiP6ceDjNedS9gjqj_yMsnS_fGc21PzEbm3ZNnJcuUMg=='.encode())
# print(a)