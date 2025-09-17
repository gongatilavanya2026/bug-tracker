# 🐞 AI Bug Tracker

A **Flask-based Bug Tracker** web application with AI-powered severity prediction for bug reports. Users can register, log in, add, edit, delete, and track bugs with an interactive dashboard showing charts by severity, status, and priority.

---

## Features

- **User Authentication**: Register, Login, and Logout securely with password hashing.
- **Bug Management**:
  - Add new bugs with AI-predicted severity.
  - Edit existing bugs, update status, priority, and assign developers.
  - Delete bugs.
- **Dashboard**:
  - Interactive charts for bug severity, status, and priority.
  - Quick statistics: total bugs, open bugs, resolved bugs.
- **Search & Filter**: Search bugs by title or description and filter by severity.
- **Responsive UI**: Modern neon-inspired theme with charts using Chart.js.

---

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **AI/ML**: Pre-trained model for predicting bug severity (`model.pkl` with `vectorizer.pkl`)
- **Libraries**:
  - Flask
  - SQLite3
  - Werkzeug (for password hashing)
  - Chart.js (for dashboards)

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/gongatilavanya2026/bug-tracker.git
cd bug-tracker
