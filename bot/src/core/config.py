import os

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    BOT_DB_USER = os.getenv('BOT_DB_USER')
    BOT_DB_PASSWORD = os.getenv('BOT_DB_PASSWORD')
    BOT_DB_HOST = os.getenv('BOT_DB_HOST')
    BOT_DB_PORT = os.getenv('BOT_DB_PORT')
    BOT_DB_NAME = os.getenv('BOT_DB_NAME')

    DATABASE_URL = f"mysql+aiomysql://{BOT_DB_USER}:{BOT_DB_PASSWORD}@{BOT_DB_HOST}:{BOT_DB_PORT}/{BOT_DB_NAME}"