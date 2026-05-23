# config.py
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
DATA_DIR = os.path.join(BASE_DIR, "Data")
os.makedirs(DATA_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, "contacts.csv")
STATE_FILE = os.path.join(DATA_DIR, "whatsapp_state.json")
LOG_FILE = os.path.join(DATA_DIR, "whatsapp_log.txt")

# Image Matching Confidence (0.0 to 1.0)
CONF_DEFAULT = 0.70
CONF_INVITE_BTN = 0.65
CONF_NO_RESULTS = 0.65

# Timing & Safety
TYPING_DELAY_MIN = 0.03
TYPING_DELAY_MAX = 0.13
CAMPAIGN_DELAY_MIN = 5   # Seconds
CAMPAIGN_DELAY_MAX = 15  # Seconds
MAX_MSG_PER_HOUR = 15