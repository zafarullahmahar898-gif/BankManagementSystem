# Bank Management System (Python + Tkinter + SQLite)

A desktop **educational simulation** of a bank: customers, accounts, deposits, withdrawals,
transfers, transaction history, customer portal, loans (simulation), reports, audit logs,
backup/restore, role-based login. Currency: **Pakistani Rupees (Rs. / PKR)**. Target: Windows 10/11.

> **Important:** this is an academic project. It is **not** production banking software
> (see [Limitations](#limitations)). Never enter real customer data, passwords or card details.

---

## 1. Features at a glance
| Area | What you get |
|---|---|
| Login | Admin & customer login, bcrypt hashing, show/hide password, lock after 5 failed attempts (15 min), session timeout (15 min), change password, forced change after admin reset |
| Dashboard | Customers, accounts, deposits, withdrawals, total balance, recent transactions, new accounts, statistics, Matplotlib chart, quick actions |
| Customers | Register, edit, search (name/ID/phone), sortable table, profile, deactivate (history is kept), create online login |
| Accounts | Auto 12-digit numbers, savings/current, initial deposit, freeze/unfreeze, close (only at zero balance), edit |
| Money | Deposit, withdraw, transfer - each with verification, confirmation dialog, receipt (save/print) |
| History | Search, type/date filters, sorting, pagination, receipt view, CSV export, immutable records |
| Portal | Customers see only their own profile, accounts, history, statements; update contact details |
| Loans | **Simulation**: apply, approve/reject, EMI schedule, repayments, outstanding balance |
| Reports | Daily/weekly/monthly deposits & withdrawals, transfers, registrations, account status, summary, balance integrity check, CSV + PDF export |
| Admin | User & role management, audit logs, failed logins, backup & restore, light/dark theme |

## 2. Quick start (Windows)
### 2.1 Install the tools
1. Install **Python 3.10+** from <https://www.python.org/downloads/> - tick **"Add python.exe to PATH"** in the installer.
2. Install **VS Code** from <https://code.visualstudio.com/>.
3. In VS Code open *Extensions* (Ctrl+Shift+X) and install **Python** (Microsoft).

### 2.2 Open the project
Unzip `BankManagementSystem.zip`, then in VS Code: **File > Open Folder...** and choose the `BankManagementSystem` folder.
Open the terminal with **Ctrl+`**.

### 2.3 Create and activate a virtual environment
PowerShell:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
If PowerShell blocks the script run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
(or simply use Command Prompt).

Command Prompt:
```bat
python -m venv venv
venv\Scripts\activate.bat
```
Your prompt should now start with `(venv)`. In VS Code press **Ctrl+Shift+P > "Python: Select Interpreter"** and choose the one inside `venv`.

### 2.4 Install dependencies
```
pip install -r requirements.txt
```

### 2.5 Create the database
The database (`data/bank.db`) is created **automatically** on first start, and tables are created/migrated by
`database/db_manager.py`. To initialise it without opening the GUI:
```
python -c "from database.db_manager import Database; print('schema version', Database().initialize())"
```

### 2.6 Create the first administrator (no password is hard-coded)
* **Option A (GUI):** run the app - on the very first start a *First-time setup* screen asks for an admin username and password.
* **Option B (terminal):** `python scripts/create_admin.py` (password is typed hidden).

### 2.7 Run
```
python main.py
```
(or double-click `run_app.bat`).  In VS Code you can also open `main.py` and press **F5**.

### 2.8 Optional fictional demo data
```
python scripts/seed_demo.py
```
Creates 5 clearly fictional customers ("Demo ..."), accounts and sample transactions, and prints random passwords
for customer logins `demo1`...`demo5` **once**. Use *Customer* login to see the portal.

## 3. How to use (short tour)
1. **Sign in** as Administrator.
2. **Customers > + New customer** (name, phone, address; email optional).
3. **Open Account**: pick the customer, type, optional initial deposit. Copy the 12-digit account number.
4. **Deposit / Withdraw / Transfer Money**: type the account number, press **Verify**, enter the amount, confirm. A receipt opens (Save, Save As, Print).
5. **Customers > Create online login** so the customer can sign in and open the **Customer Portal**.
6. **Transactions**: search, filter, sort, double-click a row for its receipt, **Export CSV**.
7. **Reports**: choose a report, period and dates, then export CSV/PDF.
8. **Database Backup**: create backups regularly.

## 4. Backup and restore
* GUI: **Database Backup > Create backup now**. Files go to `data/backups/` with a `.sha256` checksum.
* Restore: select a backup > **Restore selected backup** (or *Restore from file...*). A safety copy `pre_restore_*.db` of the current data is made first, then you are signed out.
* Manual alternative: close the app and copy `data/bank.db` somewhere safe.

## 5. Tests
```
python -m pytest -v
```
All tests use temporary databases (`tmp_path`) and never touch `data/bank.db`. They cover login/lockout, customer & account rules,
valid/invalid deposits, withdrawals, transfers, **transfer rollback**, frozen accounts, authorization, history accuracy,
immutability of records, reports (no double counting), loans, backup/restore and persistence after restart.

## 6. Security design
* Passwords: **bcrypt** (cost 12), never stored or logged in plain text; generic "invalid username or password" message.
* **Parameterized SQL everywhere**; only whitelisted column names are used for sorting.
* **Role-based access control enforced in the service layer** (the GUI hiding a button is not the only protection): customers cannot call admin operations or read other customers' data.
* Money is stored as **integer paisa** (no floats). Deposit/withdraw/transfer run in one atomic `BEGIN IMMEDIATE` transaction; a transfer debits and credits together or not at all.
* DB triggers make `transactions`, `transfers` and `audit_logs` **immutable** (no UPDATE/DELETE).
* Accounts: balance can never go negative (CHECK constraint + service check); frozen/closed accounts reject movements.
* Audit log for logins, financial operations and admin actions; failed login attempts are viewable by admins.
* CSV export neutralises spreadsheet formula injection. Errors shown to users never include stack traces (those go to `data/logs/app.log`).

## 7. Project structure
```
BankManagementSystem/
  main.py  config.py  requirements.txt  README.md  run_app.bat
  database/   schema.py (tables, indexes, triggers, migrations)  db_manager.py  backup.py
  models/     user.py customer.py account.py transaction.py
  services/   auth, customer, account, transaction, report, loan, backup, audit, ledger, permissions
  ui/         app.py login_window.py main_window.py dashboard.py customer_page.py account_page.py
              open_account_page.py deposit_page.py withdrawal_page.py transfer_page.py transaction_page.py
              portal_page.py loans_page.py reports_page.py users_page.py audit_page.py backup_page.py settings_page.py
              widgets.py theme.py charts.py lookup.py password_form.py base.py cash_form.py
  utils/      validators.py receipts.py helpers.py exceptions.py
  scripts/    create_admin.py  seed_demo.py
  tests/      conftest.py test_auth.py test_accounts.py test_transactions.py
  assets/icons/   data/ (created at runtime: bank.db, backups, receipts, exports, logs)
```
Layers: **UI -> services -> database**. The UI never writes SQL; services never import Tkinter.

## 8. Troubleshooting
| Problem | Fix |
|---|---|
| `'python' is not recognized` | Re-install Python and tick *Add to PATH*, or use `py -m venv venv`. |
| PowerShell: *running scripts is disabled* | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or use Command Prompt. |
| `ModuleNotFoundError: bcrypt / matplotlib` | Activate the venv (`(venv)` in prompt) and run `pip install -r requirements.txt`. |
| `ModuleNotFoundError: tkinter` | Re-run the Python installer > Modify > tick **tcl/tk and IDLE**. |
| `ModuleNotFoundError: config` / `services` | Run commands from the project root folder (the one containing `main.py`). |
| `database is locked` | Close other copies of the app / DB viewers that have `bank.db` open. |
| Account locked after failed logins | Wait 15 minutes, or another admin uses **User Management > Unlock**. |
| Lost the only admin password | Delete `data/bank.db` (loses all data) and run setup again, or restore a backup. |
| Blurry text on high-DPI screens | Right-click python.exe > Properties > Compatibility > *Change high DPI settings*. |
| Something looks wrong | Open `data/logs/app.log` - technical details are logged there. |

## 9. Package as a Windows executable (PyInstaller)
```
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name BankManagementSystem main.py
```
The result is `dist\BankManagementSystem.exe`. When run as an .exe the `data` folder (database, backups, logs) is created **next to the .exe**.
If antivirus flags a fresh `--onefile` build, use `--onedir` instead. Test the .exe on a copy before distributing.

## Limitations
Educational demo only: single-user local SQLite file; no encryption of the database or backups; no 2FA; no network
or multi-branch support; no KYC/AML or regulatory features; simple session handling; loan "decisions" and interest are a
simulation and not financial advice; a deactivated/removed admin's already-open window stays valid until logout or timeout.
Account rules: a customer may hold at most one open account of each type; transfers/transactions are admin (teller) operations;
customers have read-only access plus contact-detail updates and loan applications/repayments.
