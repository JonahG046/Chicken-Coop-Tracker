# 🐔 Chicken Coop Tracker

**Chicken Coop Tracker** is a Flask-based web application that helps poultry owners monitor and manage their chicken coop. Track feed, water, and egg production, visualize trends with charts, and get alerts when supplies are low.

---

## 📌 Features

- **Dashboard** with visual charts for:
  - Feed consumption (lbs)
  - Water levels (liters)
  - Egg production (count)
- **Low Level Alerts**:
  - Feed or water below threshold triggers a flashing red card with a **LOW** label.
- **API Endpoints** for logging:
  - Feed (`/api/feed`)
  - Water (`/api/water`)
  - Eggs (`/api/eggs`)
- **User Management**:
  - Registration
  - Login/Logout
- **Access Control**:
  - Only logged-in users can access the dashboard and API endpoints
- **Responsive Design**:
  - Works on desktop and mobile devices
- **Testing with Pytest**:
  - Unit tests for API endpoints, session management, and page access

---

## 🛠️ Technologies Used

- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Frontend**: HTML, CSS, Chart.js
- **Database**: SQLite (development)
- **Testing**: Pytest, pytest-flask

---

## 🚀 Getting Started

Follow these instructions to get the project running locally.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/chicken-coop-tracker.git
cd chicken-coop-tracker
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

Activate the environment:

- **Windows:**
```bash
venv\Scripts\activate
```
- **Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (Optional)
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

> On Windows PowerShell, use `set` instead of `export`:
```powershell
set FLASK_APP=app.py
set FLASK_ENV=development
```

### 5. Initialize the Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the Application
```bash
flask run
```

- Visit `http://127.0.0.1:5000/` in your browser.

---

## 📊 Dashboard Details

- Feed, water, and eggs are tracked with line charts using **Chart.js**.
- If feed is below 5 lbs or water below 2 liters, the respective card flashes red with a **LOW** label.

---

## ⚙️ API Endpoints

| Endpoint        | Method | Description                          | Auth Required |
|-----------------|--------|--------------------------------------|---------------|
| `/api/feed`     | POST   | Log feed consumption                 | Yes           |
| `/api/water`    | POST   | Log water consumption                | Yes           |
| `/api/eggs`     | POST   | Log egg production                   | Yes           |
| `/api/feed`     | GET    | Get feed logs                        | Yes           |
| `/api/water`    | GET    | Get water logs                       | Yes           |
| `/api/eggs`     | GET    | Get egg logs                         | Yes           |

---

## 🧪 Running Tests

Tests are written with **pytest**. They cover:

- Static pages (home page, redirects if not logged in)
- User authentication (registration, login, logout)
- Access control (protected pages redirect when not logged in)
- API endpoints (feed, water, egg logs can be added)
- Session management (`user_id` in session)

Run all tests:
```bash
pytest
```

---

## 📁 Project Structure

```
chicken-coop-tracker/
│
├─ app.py                  # Flask application
├─ models.py               # Database models
├─ static/                 # CSS and JS
│   └─ style.css
├─ templates/              # HTML templates
│   └─ dashboard.html
├─ tests/                  # Pytest test cases
│   └─ test_app.py
├─ __pycache__/            # Compiled Python files (should be gitignored)
├─ requirements.txt
└─ README.md
```

---

## 👤 Contributing

1. Fork the repository  
2. Create a feature branch:
```bash
git checkout -b feature/YourFeature
```
3. Commit your changes:
```bash
git commit -m "Add your message"
```
4. Push to your branch:
```bash
git push origin feature/YourFeature
```
5. Open a pull request

---

## 📜 License

MIT License – see the [LICENSE](LICENSE) file for details.

---

## 💬 Contact

