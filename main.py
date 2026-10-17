"""Entry point:  python main.py"""
import logging
import sys

import config
from database.db_manager import Database
from services import ServiceContainer


def setup_logging() -> None:
    config.ensure_directories()
    logging.basicConfig(filename=str(config.LOG_DIR / "app.log"), level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def main() -> int:
    setup_logging()
    try:
        db = Database(config.DB_PATH)
        db.initialize()
        services = ServiceContainer(db)
        from ui.app import BankApp          # imported late so a missing GUI library gives a clear message
    except ImportError as exc:
        print(f"Missing dependency: {exc}\nRun:  pip install -r requirements.txt")
        return 1
    app = BankApp(services)
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
