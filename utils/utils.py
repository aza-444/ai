from os import getenv
from dotenv import load_dotenv
load_dotenv()



class BotConfig:
    TOKEN = getenv("TOKEN")

class DBConfig:
    NAME= getenv("NAME")
    USER= getenv("USER")
    PASSWORD= getenv("PASSWORD")
    PORT= getenv("PORT")
    HOST= getenv("HOST")

class Config:
    db = DBConfig()
    bot = BotConfig()