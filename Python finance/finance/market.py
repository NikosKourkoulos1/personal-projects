from flask import Blueprint,flash, redirect, render_template, request
from cs50 import SQL
from utils import login_required, lookup

# Initialize the Blueprint
market_bp = Blueprint('market', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@market_bp.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        symbol = lookup(symbol)
        if symbol != None:
            return render_template("quoted.html", symbol=symbol)
        else:
            flash("No such symbol in the stock market")
            return redirect("/quote")