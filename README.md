# Gym Membership Management System

A BCA final-year mini project built with Python, Streamlit, SQLite, Pandas and Plotly.

## Features
- Role-based Admin and Staff login
- Member registration, search and editing
- Membership plans and configurable durations
- Membership registration and renewal
- Payment history and payment methods
- Dashboard metrics and charts
- Membership, payment and expiring-members CSV reports
- Passwords stored as salted PBKDF2 hashes

## Requirements
- Python 3.10 or newer
- pip

## Run on Windows (PowerShell)
1. Extract the project ZIP and open the folder in VS Code.
2. Open a terminal in this folder.
3. Create a virtual environment:
   `py -m venv .venv`
4. Activate it:
   `.venv\\Scripts\\Activate.ps1`
   If PowerShell blocks activation, run `.venv\\Scripts\\python.exe -m pip install -r requirements.txt` and use `.venv\\Scripts\\python.exe -m streamlit run app.py`.
5. Install dependencies:
   `python -m pip install -r requirements.txt`
6. Start the app:
   `python -m streamlit run app.py`
7. The app opens in your browser.

## First login
- Username: `admin`
- Password: `Admin@123`

Change the starter password before using real data. The current academic demo includes account creation but not a password-change page; add one before production use.

## Database
SQLite database file `gym.db` is created automatically on first run. Tables:
- `users`
- `members`
- `plans`
- `memberships`
- `payments`

## Important
This is an educational project, not a production-ready gym management platform. Add stronger deployment security, audit logs, backups, password change/reset, input validation, and privacy controls before using real customer data.
