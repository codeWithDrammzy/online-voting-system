# 🗳️ MAAUN Student E-Voting System

A secure and user-friendly Django-based voting system built for students of **Maryam Abacha American University of Nigeria (MAAUN)** to participate in departmental elections.

---

## 📸 Screenshots

| Landing Page | Login Page | Admin Dashboard |
|--------------|------------|-----------------|
| ![Landing](screenshots/home.png) | ![Login](screenshots/login.png) | ![Dashboard](screenshots/dashboard.png) |

check the screenshort folder for more



## 🚀 Features

- ✅ Student login & secure authentication
- ✅ Admin control panel to manage voters, candidates, and elections
- ✅ Role-based access control (Admin, Voter)
- ✅ Real-time voting and transparent result display
- ✅ TailwindCSS styling with clean modern UI
- ✅ Crispy form support & CSRF protection

---

## 🛠️ Tech Stack

- **Python 3**
- **Django 4+**
- **SQLite (Default) or PostgreSQL**
- **Tailwind CSS**
- **Crispy Forms (Tailwind compatible)**

---

## ✅ How to Set Up the Project Locally

### Step-by-step Guide:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/codeWithDrammzy/online-voting-system.git
cd maaun-voting-system
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install django
pip install -r requirements.txt
pip install django crispy-tailwind django-crispy-forms
