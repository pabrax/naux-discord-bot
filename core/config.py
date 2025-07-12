import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))

print(f"Token: {DISCORD_TOKEN}")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in the environment variables.")

# if not IA_TOKEN:
#     raise ValueError("IA_TOKEN is not set in the environment variables.")

