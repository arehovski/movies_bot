import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_USER = os.environ.get('PG_USER')
PG_PASS = os.environ.get('PG_PASS')
