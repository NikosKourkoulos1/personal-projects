
from flask import Blueprint, flash, render_template, request, redirect, session
from cs50 import SQL
from datetime import datetime
from utils import login_required, lookup, update_stock_prices


# Initialize the Blueprint
transactions_bp = Blueprint('transactions', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@transactions_bp.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":
        stock_name = request.form.get("symbol")
        quantity = request.form.get("shares")
        if not quantity.isdigit():
            flash("You cannot purchase partial shares")
            return redirect("/buy")
        else:
            quantity = int(request.form.get("shares"))
        stock_quote = lookup(stock_name)

        # Check for empty inputs
        if not quantity or not stock_name:
            flash("You must fill both fields")
            return redirect("/buy")
        if stock_quote == None:
            flash("Stock symbol does not exist")
            return redirect("/buy")
        if quantity <= 0:
            flash("Quantity must be a positive number")
            return redirect("/buy")

        stock_in_db = db.execute(
            "SELECT * FROM stock WHERE name = ?", stock_name.upper()
        )

        # If the stock doesn't exist, create a new row in the stocks table
        if len(stock_in_db) == 0:
            db.execute(
                "INSERT INTO stock (name, price) VALUES (?, ?)",
                stock_name.upper(),
                stock_quote["price"],
            )
            stock_id = db.execute("SELECT last_insert_rowid()")[0][
                "last_insert_rowid()"
            ]
        else:
            stock_id = stock_in_db[0]["id"]

        # Retrieve user balance
        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_balance = user_data[0]["cash"]

        # Calculate purchase cost
        purchase_cost = stock_quote["price"] * quantity

        # Check affordability
        if user_balance < purchase_cost:
            flash("You cannot afford this purchase")
            return redirect("/buy")

        # get current datetime and format it
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update user balance after purchase
        try:
            new_balance = user_balance - purchase_cost
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                new_balance,
                session["user_id"],
            )
        except:
            flash("An unexpected error occurede")
            return redirect("/buy")
        
        # Insert transaction record
        try:
            db.execute(
                """
                INSERT INTO transactions (user_id, stock_id, quantity, transaction_type, date)
                VALUES (?, ?, ?, ?, ?)
            """,
                session["user_id"],
                stock_id,
                quantity,
                "BUY",
                date,
            )
        except:
            flash("An unexpected error occurede")
            return redirect("/buy")

    return redirect("/")

@transactions_bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        # get user owned stocks
        holdings = db.execute(
            """
            SELECT stock.name, SUM(transactions.quantity) as quantity
            FROM stock
            JOIN transactions ON transactions.stock_id = stock.id
            JOIN users ON users.id = transactions.user_id
            WHERE users.id = ?
            GROUP BY stock.name
            HAVING quantity > 0;""",
            session["user_id"],
        )
        # check if the user has any stock holdings
        all_quantities_zero = True
        for stock in holdings:
            if stock["quantity"] > 0:
                all_quantities_zero = False
                break
        if all_quantities_zero:
            flash("You don't own any stocks to sell")
            return redirect("/sell")
        else:
            return render_template("sell.html", holdings=holdings)
    elif request.method == "POST":
        # get input
        stock_to_sell = request.form.get("symbol")
        quantity_to_sell = int(request.form.get("shares"))
        owned = db.execute(
            """SELECT quantity
                            FROM transactions
                            JOIN users ON transactions.user_id = users.id
                            JOIN stock ON stock.id = transactions.stock_id
                            WHERE users.id = ? and stock.name = ?""",
            session["user_id"],
            stock_to_sell,
        )

        # check if input is valid
        if quantity_to_sell <= 0 or quantity_to_sell > int(owned[0]["quantity"]):
            flash("invalid quantity to sell")
            return redirect("/sell")

        # get number of wned stocks with this name
        stock_data = db.execute(
            """
            SELECT COALESCE(SUM(transactions.quantity), 0) as owned_quantity
            FROM transactions
            JOIN stock ON stock.id = transactions.stock_id
            WHERE name = ?
            LIMIT 1""",
            stock_to_sell,
        )

        # Retrieve user balance
        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_cash = user_data[0]["cash"]

        # update stock price
        update_stock_prices(db)

        # get stock price
        stock_data = db.execute(
            "SELECT id, price FROM stock WHERE name = ?", stock_to_sell
        )
        stock_price = stock_data[0]["price"]

        # update user cash
        try:
            user_cash = user_cash + stock_price * quantity_to_sell
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", user_cash, session["user_id"]
            )
        except:
            flash("An unexpected error occured")
            return redirect("/sell")

        # insert sell transaction record (negative quantity for sell)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            db.execute(
                """
                INSERT INTO transactions (user_id, stock_id, quantity, transaction_type, date)
                VALUES (?, ?, ?, ?, ?)
            """,
                session["user_id"],
                stock_data[0]["id"],
                -quantity_to_sell,
                "SELL",
                date,
            )
        except:
            flash("An unexpected error occured")
            return redirect("/sell")

    return redirect("/")


@transactions_bp.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    print(request.method)
    if request.method == "GET":
        return render_template("add_cash.html")
    elif request.method == "POST":
        aditional_cash = request.form.get("cash_amount")
        # Retrieve user balance
        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_cash = user_data[0]["cash"]
        new_cash_balance = user_cash + int(aditional_cash)
        print(new_cash_balance)
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            new_cash_balance,
            session["user_id"],
        )
        return redirect("/")
    

@transactions_bp.route("/withdraw_cash", methods=["GET", "POST"])
@login_required
def withdraw_cash():
    if request.method == "GET":
        return render_template("withdraw_cash.html")
    elif request.method == "POST":
        withdrawal_amount = request.form.get("cash_amount")

        # Retrieve user balance
        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        user_cash = user_data[0]["cash"]

        # Check if the user has enough cash to withdraw
        if int(withdrawal_amount) > user_cash:
            flash("Insufficient balance to withdraw this ammount", "error")
            return redirect("/withdraw_cash")

        # Update the user's cash balance
        new_cash_balance = user_cash - int(withdrawal_amount)
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            new_cash_balance,
            session["user_id"]
        )

        flash("Withdrawal successful", "success")
        return redirect("/")


@transactions_bp.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute(
        """
        SELECT
        stock.name as stock_symbol,
        stock.price,
        transactions.transaction_type ,
        transactions.quantity ,
        transactions.date
        FROM stock
        JOIN transactions ON transactions.stock_id = stock.id
        JOIN users ON users.id = transactions.user_id
        WHERE users.id = ?""",
        session["user_id"],
    )
    for row in history:
        # Make quantity positive if it's negative
        if row["quantity"] < 0:
            row["quantity"] = abs(row["quantity"])

        # Calculate total price
        row["total_price"] = row["quantity"] * row["price"]
        
    return render_template("/history.html", history=history)    