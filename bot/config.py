import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SITE_URL = os.environ.get("SITE_URL")
