# Basic Password Manager

A simple and secure **Password Manager** built using **PySide6 (Qt for Python)**. This application allows you to **create, save, and manage your passwords**, making it easy to sign in to websites and apps.

## Features
- **User Authentication**: Sign up, log in, and reset your password.
- **Secure Storage**: Save passwords securely.
- **Encryption**: Uses **Fernet encryption (from the cryptography library)** to securely encrypt and decrypt stored passwords.
- **Password Retrieval**: Easily retrieve stored passwords.
- **Simple UI**: User-friendly graphical interface built with PySide6.

## Installation
### Prerequisites
- Python 3.x
- PySide6
- cryptography (for encryption)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yashraj-kumawat-14/basic-password-manager
   cd basic-password-manager
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root directory and add the following environment variables:
   ```ini
   DB_NAME=your_database_name
   EMAIL_SENDER=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   SECRET_KEY=your_secret_key_for_fernet
   ```
5. Run the application:
   ```bash
   python main.py
   ```

## Usage
- **Sign Up**: Create a new account.
- **Log In**: Access saved passwords using your credentials.
- **Forgot Password**: Reset your password if forgotten.

## Technologies Used
- **Python** (Backend Logic)
- **PySide6 (Qt for Python)** (GUI Development)
- **SQLite** (Database for storing user credentials and passwords)
- **Fernet Encryption** (Encrypting and decrypting passwords securely)

## Contributing
Feel free to submit issues and pull requests to improve the project.

## License
This project is licensed under the MIT License.

## Screenshots

### Login Screen
![Login Screen](screenshots/login.png)

### Signup Screen
![Signup Screen](screenshots/signup.png)

### Password Manager Dashboard
![Dashboard](screenshots/dashboard.png)

### Add Password
![Add Password](screenshots/add.png)

### View Password
![View Password](screenshots/view.png)

---
A vault of security 🔒, crafted by Yashraj

