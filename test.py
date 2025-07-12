import os

from dotenv import load_dotenv

load_dotenv()

allowed_users = os.getenv("ALLOWED_USERS").split(",")
print(allowed_users)
