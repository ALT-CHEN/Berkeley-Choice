import os
import secrets

class Config:
    SECRET_KEY_FILE = ".secret_key"  # File to store the secret key

    # Try to get SECRET_KEY from environment variable
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # If SECRET_KEY is not set, check if a key exists in the file
    if not SECRET_KEY:
        if os.path.exists(SECRET_KEY_FILE):
            with open(SECRET_KEY_FILE, "r") as f:
                SECRET_KEY = f.read().strip()  # Load the existing key
        else:
            # Generate a new key and save it
            SECRET_KEY = secrets.token_hex(32)
            with open(SECRET_KEY_FILE, "w") as f:
                f.write(SECRET_KEY)

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
