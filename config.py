"""Central configuration for the Bank Management System (educational project)."""
import os
import sys
from pathlib import Path

# When packaged with PyInstaller the data folder lives next to the .exe.
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = Path(os.environ.get("BMS_DATA_DIR", BASE_DIR / "data"))
DB_PATH = Path(os.environ.get("BMS_DB_PATH", DATA_DIR / "bank.db"))
BACKUP_DIR = DATA_DIR / "backups"
RECEIPT_DIR = DATA_DIR / "receipts"
EXPORT_DIR = DATA_DIR / "exports"
LOG_DIR = DATA_DIR / "logs"

APP_NAME = "Bank Management System"
APP_VERSION = "1.0.0"
CURRENCY_SYMBOL = "Rs."
CURRENCY_CODE = "PKR"

# --- Security -------------------------------------------------------------
MAX_LOGIN_ATTEMPTS = 5          # failed attempts before the account is locked
LOCKOUT_MINUTES = 15            # how long a lock lasts
SESSION_TIMEOUT_MINUTES = 15    # inactivity timeout
MIN_PASSWORD_LENGTH = 8
BCRYPT_ROUNDS = 12

# --- Money (all amounts are stored as integer paisa; 100 paisa = Rs. 1) ----
MAX_TRANSACTION_PAISA = 100_000_000 * 100   # Rs. 100,000,000 per transaction

# --- Loans (simulation only) ----------------------------------------------
LOAN_DEFAULT_ANNUAL_RATE = 12.0
LOAN_MIN_PAISA = 1_000 * 100
LOAN_MAX_PAISA = 10_000_000 * 100
LOAN_MAX_TERM_MONTHS = 60

PAGE_SIZE = 25


def ensure_directories() -> None:
    """Create the data folders on first run."""
    for folder in (DATA_DIR, BACKUP_DIR, RECEIPT_DIR, EXPORT_DIR, LOG_DIR):
        folder.mkdir(parents=True, exist_ok=True)
