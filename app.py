from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///system.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("name"):
        return redirect("/login-page")
    if request.method == "POST":

        message = request.form.get("message")
        name = session["name"]
        db.execute("INSERT INTO messages (message_text, message_name) VALUES(?, ?)", message, name)

        return redirect("/")

    else:
        notes = db.execute("SELECT * FROM messages ORDER BY timestamp DESC")
        return render_template("index.html", notes=notes, name=session.get("name"))

@app.route("/clear", methods=["GET", "POST"])
def clear():
    if session["name"] == "TheMidnightWolf":
        db.execute("DELETE FROM messages;")
        return jsonify({"success": True})

    return jsonify({"success": True})

@app.route("/login", methods=["GET", "POST"])
def name():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if db.execute("SELECT username FROM users WHERE username = ? AND password = ?", username, password):
            session["name"] = username
            return redirect("/")
    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/signup-page", methods=["GET", "POST"])
def signuppage():
    return render_template("signup.html")

@app.route("/login-page", methods=["GET", "POST"])
def loginpage():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if not db.execute("SELECT username FROM users WHERE username = ? AND email = ?", username, email):
        db.execute("INSERT INTO users (username, password, email) VALUES(?, ?, ?)", username, password, email)
        session["name"] = username
        return redirect("/")
    return render_template("signup.html")

@app.route('/get_messages')
def get_messages():
    messages = db.execute("SELECT message_name, message_text FROM messages ORDER BY timestamp DESC")
    # Convert the SQL rows to dictionaries
    messages_list = [dict(row) for row in messages]
    return jsonify({'messages': messages_list})

@app.route("/p-change", methods=["GET", "POST"])
def passwordChange():
    password = request.form.get("password")
    name = session["name"]
    np1 = request.form.get("npassword")
    np2 = request.form.get("n2password")

    if db.execute("SELECT * FROM users WHERE username = ? AND password = ?", name, password):
        if (np2 == np1):
            db.execute("UPDATE users SET password = ? WHERE username = ?", np1, name)
            return render_template("profile.html")
        else:
            error = "Passwords incorrect."
            return render_template("error.html", error=error)
    else:
        error = "Passwords incorrect."
        return render_template("error.html", error=error)

@app.route('/send', methods=['POST'])
def send_message():
    message = request.form.get("message")
    name = session["name"]
    db.execute("INSERT INTO messages (message_text, message_name) VALUES(?, ?)", message, name)
    return jsonify({"success": True})

@app.route("/profile", methods=["GET","POST"])
def profile():
    name = session["name"]

    return render_template("profile.html", name=name)

@app.route("/home", methods=["GET","POST"])
def home():
    name = session["name"]

    return render_template("index.html", name=name)