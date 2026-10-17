
import getpass
import config
from database.db_manager import Database
from services.auth_service import AuthService

def main():
    db = Database(config.DB_PATH)

    admins = db.fetch_all(
        "SELECT id, username FROM users WHERE role = 'admin' ORDER BY id"
    )

    if not admins:
        print("Koi admin account nahi mila.")
        return

    print("Admin accounts:")
    for admin in admins:
        print(f"ID: {admin['id']} | Username: {admin['username']}")

    username = input("Apna admin username likhein: ").strip()
    matches = [a for a in admins if a["username"] == username]

    if len(matches) != 1:
        print("Username match nahi hua. Koi change nahi kiya.")
        return

    password = getpass.getpass("Naya password (kam az kam 8 characters): ")
    confirm = getpass.getpass("Naya password dobara likhein: ")

    if password != confirm:
        print("Passwords match nahi hue. Koi change nahi kiya.")
        return

    auth = AuthService(db)
    admin = matches[0]

    from utils import validators
    validators.validate_password(password, username)

    with db.transaction() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ?, must_change_password = 1, "
            "failed_attempts = 0, locked_until = NULL WHERE id = ? AND role = 'admin'",
            (auth.hash_password(password), admin["id"])
        )

    print("Password successfully reset ho gaya.")
    print("Ab app mein admin username aur naya password use karein.")

if __name__ == "__main__":
    main()
