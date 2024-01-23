from flask import Blueprint, flash, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

# Initialize the Blueprint
auth_bp = Blueprint('auth', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide username")
            return redirect("/login")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return redirect("/login")


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username or not password or not confirm_password:
            flash("Please fill all three fields to continue ")
            return redirect("/register")
        elif password != confirm_password:
            flash("Passwords don't match ")
            return redirect("/register")

        hash = generate_password_hash(password)
        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )
        except:
            flash("Username is not available, please try a new username")
            return redirect("/register")

        # Log in the user automatically after registration
        session["user_id"] = new_user

        return redirect("/")
