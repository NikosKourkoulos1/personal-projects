from flask import Blueprint, render_template, request, redirect, session
from cs50 import SQL
from utils import login_required, update_stock_prices


# Initialize the Blueprint
portfolio_bp = Blueprint('portfolio', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@portfolio_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        # get user cash
        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_cash = user_data[0]["cash"]
        print(user_cash)
        # query to display hodings
        owned_stocks = db.execute(
            """
            SELECT stock.name as stock_name,
                SUM(transactions.quantity) as stock_quantity
            FROM stock
            JOIN transactions ON stock.id = transactions.stock_id
            JOIN users ON users.id = transactions.user_id
            WHERE users.id = ?
            GROUP BY stock_name
        """,
            session["user_id"],
        )

        # call helper method to update the stock prices
        update_stock_prices(db)

        # get user current cash balance
        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_cash = user_data[0]["cash"]
        # initialise total balance
        total_balance = user_cash
        # addkeys price and total value to the owned_stocks dictionary
        # update total user balance
        for stock in owned_stocks:
            stock_data = db.execute(
                "SELECT price FROM stock WHERE name = ?", stock["stock_name"]
            )
            stock_price = stock_data[0]["price"]
            stock["current_price"] = stock_price
            stock["total_value"] = round(stock["stock_quantity"] * stock_price, 2)
            total_balance += stock["total_value"]
            print(total_balance)
        return render_template(
            "index.html",
            owned_stocks=owned_stocks,
            user_cash=round(user_cash, 2),
            total_balance=round(total_balance, 2),
        )
    elif request.method == "POST":
        return redirect("/add_cash")
