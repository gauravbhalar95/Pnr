import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Telegram Bot Token is missing!")

print("Bot Token Loaded Successfully!")
