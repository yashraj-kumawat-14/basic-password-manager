import os

# Define the .env filename
ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
print(ENV_FILE_PATH)

# Default environment variables
DEFAULT_ENV_VARS = {
    "EMAIL_SENDER": "yantrigo14@gmail.com",
    "EMAIL_PASSWORD": "rbvxlvqtjlhyimyi",
    "DB_NAME":"password_manager.db",
    "SECRET_KEY":"4kb3o9-jhSx8JIiMFoAdnKkGn1QEaJSilAFxY3hyzy8="
}

def create_env_file():
    """Creates a .env file if it does not exist and adds default values."""
    if not os.path.exists(ENV_FILE_PATH):
        with open(ENV_FILE_PATH, "w") as env_file:
            for key, value in DEFAULT_ENV_VARS.items():
                env_file.write(f"{key}={value}\n")
        print(f"{ENV_FILE_PATH} created with default values. Please update it with actual credentials.")
    else:
        print(f"{ENV_FILE_PATH} already exists. No changes made.")

if __name__ == "__main__":
    create_env_file()
