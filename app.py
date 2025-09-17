from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from predict import predict_severity
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "bugtracker_secret"
DB_NAME = "bugs.db"

# --- Helper function ---
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ================= USER AUTH ROUTES =================

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not all([username, email, password, confirm_password]):
            flash("All fields are required!", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        conn = get_db_connection()
        existing_user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if existing_user:
            flash("Email already registered!", "danger")
            conn.close()
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     (username, email, hashed_pw))
        conn.commit()
        conn.close()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not all([email, password]):
            flash("Email and password are required!", "danger")
            return redirect(url_for("login"))

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Welcome, {user['username']}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# ================= BUG TRACKER ROUTES =================

# --- READ (Home + Search) ---
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    query = request.args.get("q", "")
    filter_severity = request.args.get("filter", "")
    conn = get_db_connection()
    sql = "SELECT * FROM bugs WHERE title LIKE ? OR description LIKE ?"
    params = (f"%{query}%", f"%{query}%")
    if filter_severity:
        sql += " AND severity=?"
        params += (filter_severity,)
    sql += " ORDER BY created_at DESC"
    bugs = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template("index.html", bugs=bugs)

# --- CREATE (Add Bug) ---
@app.route("/add", methods=["POST"])
def add_bug():
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title")
    description = request.form.get("description")
    severity = predict_severity(description) if description else "Low"
    priority = request.form.get("priority", "Low")
    assignee = request.form.get("assignee", "")

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO bugs (title, description, severity, priority, assignee, status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, severity, priority, assignee, "Open", datetime.now()))
    conn.commit()
    conn.close()
    flash(f"Bug added successfully! Predicted Severity: {severity}", "success")
    return redirect(url_for("index"))

# --- UPDATE (Edit Bug) ---
@app.route("/edit/<int:bug_id>", methods=["GET", "POST"])
def edit_bug(bug_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    bug = conn.execute("SELECT * FROM bugs WHERE id=?", (bug_id,)).fetchone()
    if not bug:
        flash("Bug not found!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        severity = request.form.get("severity")
        status = request.form.get("status")
        priority = request.form.get("priority")
        assignee = request.form.get("assignee")

        conn.execute("""
            UPDATE bugs 
            SET title=?, description=?, severity=?, status=?, priority=?, assignee=?, updated_at=?
            WHERE id=?
        """, (title, description, severity, status, priority, assignee, datetime.now(), bug_id))
        conn.commit()
        conn.close()
        flash("Bug updated successfully!", "info")
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", bug=bug)

# --- DASHBOARD ---
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    
    severity_counts = conn.execute("SELECT severity, COUNT(*) as count FROM bugs GROUP BY severity").fetchall()
    status_counts = conn.execute("SELECT status, COUNT(*) as count FROM bugs GROUP BY status").fetchall()
    priority_counts = conn.execute("SELECT priority, COUNT(*) as count FROM bugs GROUP BY priority").fetchall()
    
    total_bugs = conn.execute("SELECT COUNT(*) FROM bugs").fetchone()[0]
    open_bugs = conn.execute("SELECT COUNT(*) FROM bugs WHERE status='Open'").fetchone()[0]
    resolved_bugs = conn.execute("SELECT COUNT(*) FROM bugs WHERE status='Resolved'").fetchone()[0]
    
    conn.close()
    
    return render_template(
        "dashboard.html",
        severity_counts=severity_counts,
        status_counts=status_counts,
        priority_counts=priority_counts,
        total_bugs=total_bugs,
        open_bugs=open_bugs,
        resolved_bugs=resolved_bugs
    )

# --- DELETE BUG ---
@app.route("/delete/<int:bug_id>", methods=["POST"])
def delete_bug(bug_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.execute("DELETE FROM bugs WHERE id=?", (bug_id,))
    conn.commit()
    conn.close()
    flash("Bug deleted successfully!", "danger")
    return redirect(url_for("index"))

# --- UPDATE STATUS ---
@app.route("/update_status/<int:bug_id>/<new_status>", methods=["POST"])
def update_status(bug_id, new_status):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.execute("UPDATE bugs SET status=?, updated_at=? WHERE id=?", (new_status, datetime.now(), bug_id))
    conn.commit()
    conn.close()
    flash(f"Bug status updated to {new_status}", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
