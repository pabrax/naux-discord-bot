import sys
import pathlib

# Ensure repo root is on sys.path so the 'bot' package is importable when run from repo root
ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bot.main import main as run_bot


if __name__ == "__main__":
    run_bot()
