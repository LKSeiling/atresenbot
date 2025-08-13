import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GROUP_ID = int(os.getenv("GROUP_ID", "0"))
PLENUM_WEEKDAY = os.getenv("PLENUM_WEEKDAY", "Friday")
TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Europe/Berlin"))

# Webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
PORT = int(os.getenv("PORT", "8443"))
LISTEN_ADDR = os.getenv("LISTEN_ADDR", "0.0.0.0")

# Dateien
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TOPS_FILE = os.path.join(DATA_DIR, "tops.json")
ADMINS_FILE = os.path.join(DATA_DIR, "admins.json")

os.makedirs(DATA_DIR, exist_ok=True)