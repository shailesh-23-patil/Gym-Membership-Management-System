# 🏋️ Gym Membership Management System

A beginner-friendly web application built with **Python, Streamlit, and SQLite** to manage gym members, membership plans, registrations, payments, and reports.

<p align="center">
  <strong>Simple • Organized • User-Friendly</strong>
</p>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [How to Run the Project](#-how-to-run-the-project)
- [How to Use the Web Application](#-how-to-use-the-web-application)
- [User Roles](#-user-roles)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

## 📖 About the Project

Managing a gym manually can be time-consuming. Gym staff need to maintain member details, membership plans, payment records, and other important information.

The **Gym Membership Management System** provides a centralized web application to simplify these tasks. It allows authorized users to manage gym-related information through a browser instead of relying entirely on manual records.

This project was developed as an academic mini project to demonstrate Python programming, database management, authentication, and web application development.

## ✨ Features

- 📊 **Dashboard:** View gym management summaries and available charts.
- 👥 **Member Management:** Register, search, view, and update member information.
- 📋 **Membership Plans:** View and manage available plans.
- 📝 **Membership Registration:** Associate members with membership plans.
- 💳 **Payment Management:** Record and view payment information.
- 📈 **Reports:** Review records and download supported reports in CSV format.
- 🔐 **Role-Based Authentication:** Separate Admin and Staff access.
- 🗄️ **SQLite Database:** Store application data locally.
- 🌐 **Browser-Based Interface:** Use the application through a web browser.
- 📂 **Automatic Database Initialization:** The application can initialize its local database when configured to do so.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| SQLite | Local database |
| Pandas | Data handling and tabular reports |
| Matplotlib / Seaborn | Data visualization, where used |
| Git and GitHub | Version control and project hosting |

## 📁 Project Structure

```text
Gym-Membership-Management-System/
│
├── app.py
├── auth.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── dashboard.png
    ├── login.png
    ├── member.png
    ├── membership_plans.png
    └── payments.png
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Main Streamlit application |
| `auth.py` | Authentication and access control |
| `database.py` | Database initialization and operations |
| `requirements.txt` | Required Python packages |
| `README.md` | Project documentation |
| `.gitignore` | Excludes selected local and sensitive files |
| `screenshots/` | Application screenshots |

The SQLite database is stored locally and should not be uploaded to the public repository.

---

## 🚀 Installation and Setup

Follow these instructions to download and run the project on your computer.

### Prerequisites

Before starting, install:

- **Python:** A version compatible with the packages in `requirements.txt`
- **VS Code:** Recommended code editor
- **Git:** Optional if you download the ZIP file instead of cloning the repository
- **Web browser:** Chrome, Edge, Firefox, or another modern browser

Download Python: https://www.python.org/downloads/

Download VS Code: https://code.visualstudio.com/

### Step 1: Download the Project

**Option A — Download ZIP**

1. Open the [GitHub repository](https://github.com/shailesh-23-patil/Gym-Membership-Management-System).
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Open the extracted folder in VS Code.

**Option B — Clone Using Git**

Open PowerShell, Command Prompt, or the VS Code terminal and run:

```bash
git clone https://github.com/shailesh-23-patil/Gym-Membership-Management-System.git
```

Move into the project folder:

```bash
cd Gym-Membership-Management-System
```

### Step 2: Open the Project Terminal

Open the project folder in VS Code.

Select **Terminal → New Terminal** from the menu.

Ensure the terminal is in the directory containing `app.py`.

### Step 3: Create a Virtual Environment

A virtual environment keeps this project's Python packages separate from other projects.

For Windows:

```powershell
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

After activation, you should see `(.venv)` at the beginning of the terminal prompt.

If PowerShell blocks activation, you can use Command Prompt or run this command in the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### Step 5: Install the Required Packages

Run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Wait until the installation completes.

### Step 6: Verify the Project Files

Make sure the main project files are present:

```text
app.py
auth.py
database.py
requirements.txt
```

If any required file is missing, the application may fail to start.

---

## ▶️ How to Run the Project

After installing the dependencies, start the application with:

```bash
python -m streamlit run app.py
```

Streamlit will start a local web server and display a URL in the terminal.

The default address is usually:

http://localhost:8501

Open the URL in your browser if it does not open automatically.

Keep the terminal running while using the application. To stop the server, press `Ctrl + C` in the terminal.

**🎉 Your Gym Membership Management System is ready to explore!**

---

## 🖥️ How to Use the Web Application

After opening the application in your browser, follow these steps to explore its functionality.

### 1. 🔐 Login to the Application

- Open the application URL in your browser.
- Enter your username and password.
- Log in using an account configured for your application.
- Access the features available to your assigned role.

Use the credentials configured in the application. Do not assume that a default account exists unless it is defined in the source code.

### 2. 📊 Explore the Dashboard

The dashboard provides an overview of the information managed by the system.

- Review the available summary cards.
- Explore the charts and statistics.
- Use the dashboard to understand the current records in the application.

The displayed metrics depend on the data stored in the local database.

### 3. 👥 Manage Gym Members

Open the member management section.

- Register a new gym member.
- Enter the required member details.
- Search for existing members.
- View member information.
- Update details when necessary.

Always verify the information before saving.

### 4. 📋 Manage Membership Plans

Open the membership plans section.

- View the available membership plans.
- Review plan details and pricing.
- Add or update plans if your role has permission to do so.

The available operations depend on the application's implementation.

### 5. 📝 Register Memberships

Use the membership registration functionality to associate a member with a plan.

1. Open the relevant membership section.
2. Select the appropriate member.
3. Choose an available membership plan.
4. Enter the required details.
5. Save the registration.
6. Verify the resulting record.

### 6. 💳 Manage Payments

Open the payment management section.

- Record payment information where permitted.
- Review available payment records.
- Check the associated member and payment details.
- Verify the information after saving.

Use sample payment data while testing the project.

### 7. 📈 View Reports and Export Data

Open the reports section.

- Review the reports available in the application.
- Examine the relevant records and summaries.
- Download supported reports using the available CSV download options.
- Open downloaded CSV files using Microsoft Excel or another spreadsheet application.

### 8. 👤 Use Admin and Staff Accounts

The application supports role-based access.

- **Admin:** Can access administrative functions, including user management where implemented.
- **Staff:** Can access the gym management features allowed by the application's permissions.

Some functions may be restricted depending on the logged-in user's role.

### 9. 🚪 Logout

When you finish using the application, use the logout option if it is provided by the interface.

Close the browser tab when finished.

### 💡 Tips for First-Time Users

- Start with sample data.
- Explore the dashboard before entering records.
- Use test member details while learning the application.
- Verify payment and membership details before saving.
- Keep login credentials private.
- Do not enter real personal information into a publicly accessible demonstration application.

*Note: Available screens and actions depend on the functionality implemented in the current source code.*

---

## 🔐 User Roles and Security

The system supports Admin and Staff roles with role-based access to application features.

For safer use:

- Do not share passwords or private credentials.
- Change any demo or default password before using the application with real data.
- Do not commit the local database file to GitHub.
- Do not upload real member information or secrets.
- Review authentication and authorization before deploying the application online.

This project is intended for educational use and should not be considered production-ready without additional security review.

---

## 📸 Screenshots

The following screenshots demonstrate the application's interface.

### 🔑 Login Page

![Login Page](screenshots/login.png)

### 📊 Dashboard

![Dashboard](screenshots/dashboard.png)

### 👥 Member Management

![Member Management](screenshots/member.png)

### 📋 Membership Plans

![Membership Plans](screenshots/membership_plans.png)

### 💳 Payment Management

![Payments](screenshots/payments.png)

**Privacy reminder:** Use sample data in screenshots published on GitHub. Remove or blur real names, phone numbers, email addresses, and other private information.

---

## 🧰 Troubleshooting

### Problem 1: Python Is Not Recognized

Check whether Python is installed:

```bash
python --version
```

On Windows, you can also try:

```bash
py --version
```

If neither command works, install Python and ensure it is available in PATH.

### Problem 2: Streamlit Is Not Recognized

Activate the virtual environment and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start Streamlit using:

```bash
python -m streamlit run app.py
```

### Problem 3: The Application Does Not Open

Check the terminal for error messages.

Try opening the default local address manually:

http://localhost:8501

Make sure the Streamlit process is still running.

### Problem 4: Missing Module Error

If Python reports that a module is missing, activate the virtual environment and run:

```bash
pip install -r requirements.txt
```

### Problem 5: Database Error

Check that:

- The project folder is writable.
- `database.py` is present.
- The database initialization code runs correctly.
- The application is using the expected database path.

The local database may be generated automatically depending on the initialization logic.

### Problem 6: Login Does Not Work

Check the account setup and authentication logic in `auth.py` and the related database functions.

Use only credentials configured for your local application. Do not publish passwords or database files to resolve login issues.

### Problem 7: Port 8501 Is Already in Use

Start the application using another port:

```bash
python -m streamlit run app.py --server.port 8502
```

Open:

http://localhost:8502

---

## 🔮 Future Enhancements

Possible future improvements include:

- 📅 Membership expiry notifications
- 🔔 Automatic renewal reminders
- 📄 PDF report generation
- 🔑 Password change and password reset functionality
- 📊 Improved dashboard analytics
- 💰 Enhanced payment summaries
- ☁️ Secure cloud deployment
- 🛡️ Additional security and access-control improvements

These are proposed improvements and may not be available in the current version.

---

## 👨‍💻 Author

**Shailesh Patil**

- GitHub Profile: [shailesh-23-patil](https://github.com/shailesh-23-patil)
- Project Repository: [Gym Membership Management System](https://github.com/shailesh-23-patil/Gym-Membership-Management-System)

---

## ⭐ Support

If you find this project helpful for learning, feel free to explore the source code and build upon it.

If you use this project as a learning reference, consider giving the repository a ⭐ on GitHub.

## 📜 Disclaimer

This project was developed for academic and educational purposes. Review the application's authentication, data protection, database management, and deployment security before using it with real gym members.
