import os


class Config:
    SECRET_KEY = "your_secret_key_here"
    DB_URI = os.environ.get(
        "DB_URL", "postgresql://username:password@localhost:5432/shiva-pot"
    )
