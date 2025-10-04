import os
from dotenv import load_dotenv

load_dotenv()

# Discord configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))
PREFIX = os.getenv("PREFIX", "!")

print(f"Discord Token: {DISCORD_TOKEN}")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in the environment variables.")


# IA configuration
class IaSettings:
    IA_MODEL_NAME = os.getenv("IA_MODEL_NAME")
    IA_API_KEY = os.getenv("IA_API_KEY")
    IA_API_URL = os.getenv("IA_API_URL")

# Ensure IA settings are loaded correctly
ia_settings = IaSettings()
