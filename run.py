import threading
from bot.main import run_bot
from api.fastapi_app import start_fastapi

# Start FastAPI in a separate thread
threading.Thread(target=start_fastapi, daemon=True).start()
run_bot()
