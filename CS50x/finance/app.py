import os
import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

########### SCHEMA ###########
# CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
# CREATE TABLE sqlite_sequence(name,seq);
# CREATE UNIQUE INDEX username ON users (username);

#TABLE shares(user_id INTEGER, s_name TEXT NOT NULL, s_num INTEGER NOT NULL, price INTEGER NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (s_username) REFERENCES users(username))

# Make sure API key is set
# export API_KEY=pk_87490551bce7446da6f4c820100e6092
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

db.execute("CREATE TABLE IF NOT EXISTS shares(user_id INTEGER, s_name TEXT NOT NULL, s_num INTEGER NOT NULL, price INTEGER NOT NULL, total INTEGER NOT NULL, symbol TEXT NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




#TABLE shares(user_id INTEGER, s_name TEXT NOT NULL, s_num INTEGER NOT NULL, price INTEGER NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (s_username) REFERENCES users(username))
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]  #유저 id

#밑에 다필요없고 WHERE = user_id 일치하고 stock name으로 통합된 하나의 리스트만 있으면 index 만들 수 있음.
    stocks = db.execute("SELECT symbol, s_name, SUM(s_num), price FROM shares WHERE user_id = ? GROUP BY s_name ORDER BY s_name", user_id) #로그인된 유저의 stock(중복된거 합침)
    total = db.execute("SELECT SUM(total) FROM shares WHERE user_id = ? GROUP BY s_name", user_id) #로그인된 유저의 stock(중복된거 합침)
    cashs = db.execute("SELECT * FROM users WHERE id = ? ", user_id)
    # db.execute("DELETE FROM shares WHERE s_num = 0")
    print("@@@@@@@$")
    print(total)
    print(cashs)
    # shares = db.execute("SELECT SUM(s_num) FROM shares WHERE user_id = ? GROUP BY s_name ORDER BY s_name", user_id)  # stock 별 갯수
    # name = db.execute("SELECT s_name FROM shares WHERE user_id = ? GROUP BY s_name ORDER BY s_name", user_id) #로그인된 유저의 stock(중복된거 합침)
    # price = db.execute("SELECT price FROM shares WHERE user_id = ? GROUP BY s_name ORDER BY s_name", user_id)

    print("$$$$$$$$$$$$$$$", total)
    return render_template("index.html", stocks=stocks, cashs=cashs, total=total) # ,shares=shares, name=name, symbol=symbol, total=total)
    # if not total:
    #     return render_template("index.html", stocks=stocks, cashs=cashs, total=total) # ,shares=shares, name=name, symbol=symbol, total=total)
    # # index.html사용하면 /index가 아니라 /  로 뜬다. 왜그런지 모르겠음
    # elif total:
    #     return render_template("index.html", stocks=stocks, cashs=cashs, total=total) # ,shares=shares, name=name, symbol=symbol, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        user = session["user_id"]  #user_id 세션은 username이 아니라 id다.
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user)[0]["cash"]

        print(type(shares)) # 역시 str이다.

        if lookup(symbol) != None:
            stockname = lookup(symbol)["name"] #여기서 버그생긴 이유 = lookup의 결과가 None인 경우 lookup(symbol) == None이고
            price = lookup(symbol)["price"]    #lookup(symbol)["price, name 등"] 은 None이아니라 존재하지도 않음. helpers.py 보면 알수있음


        if symbol == None or shares == None:
            return apology("Need Input!", 400)
        #문제생기는 이유 1. html input="number"로 해도 string이다. 2. check50는 HTML과 무관하게 값을 입력값을 정함
        elif shares.isdigit() == False :
            return apology("Shares should be a number !", 400)
        elif float(shares).is_integer() == False :
            return apology("Shares should not be fractional !", 400)
        elif float(shares) < 1 :
            return apology("Shares should be an int over 0 !", 400)

        elif lookup(symbol) == None:
            return apology("Stock doesn't exist!", 400)
        else:
            if int(shares) * price > cash: #잔고 부족하면 apology , db.excute해서 얻은 데이터가 list형태로 있어 직접적인 비교가 불가능한 문제가 있었음
                return apology("NOT ENOUGH MINERALS", 400)

            else: #db.execute("SELECT * FROM shares") == None:                                #잔고 안부족하면 share 테이블 만들어주기
                cash = cash - int(shares) * price

                db.execute("INSERT INTO shares (user_id, s_name, s_num, price, total, symbol) VALUES(?,? , ?, ?, ?, ?)", user, stockname, int(shares), price, int(shares)*price, lookup(symbol)["symbol"])
                #sqlite symbol 업데이트할때 symbol 첫글자로 하면 symbol AC A 이런경우 겹쳐서 sell buy 시 버그발생함 고쳐주니 sell 문제 해결
                
                db.execute("UPDATE users SET cash = ? WHERE id = ? ",cash ,user)
                return redirect("/")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    user = session["user_id"]
    """Show history of transactions"""
    history = db.execute("SELECT * FROM shares WHERE user_id = ? ORDER BY Timestamp",user)

    # print(history["symbol"])

    return render_template("history.html", history = history)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        search = lookup(request.form.get("symbol"))
        if search == None:
            return apology("Doesn't exist")
        else:
            return render_template("quote.html",search=search)
    else:
        return render_template("quote.html")


##
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)

        if not username.strip() or not password.strip():
            return apology("Need Input!", 400)
        elif password != confirmation:
            return apology("Check password!", 400)
        elif db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("Username already exists!", 400)

        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

            return redirect("/")

    else:
        return render_template("register.html")



# 해야 할 것 = sell 오류 등, input forloop로 SELECT symbol FROM shares WHERE user_id = ? , user 로 html에 넣어서 돌림

#TABLE shares(user_id INTEGER, s_name TEXT NOT NULL, s_num INTEGER NOT NULL, price INTEGER NOT NULL, total INTEGER NOT NULL, symbol TEXT NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))")
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user = session["user_id"]  #user_id 세션은 username이 아니라 id다.
    if request.method == "POST":
        symbol = request.form.get("symbol")
        share = request.form.get("shares")
        cmpshares = db.execute("SELECT SUM(s_num) FROM shares WHERE user_id = ? AND symbol = ? GROUP BY s_name", user, symbol)

        print(cmpshares)

        if symbol == None or share == None: #입력없으면 error
            return apology("Need input!", 400)
        elif share.isdigit() == False:         #shares에 숫자 아니면 error
            return apology("shares must be integer!", 400)
        elif float(share).is_integer() == False:  #int 아니면 거름
            return apology("shares must be integer!", 400)
        elif int(share) < 1 :                    #1 미만이면 거름
            return apology("Shares should be an int over 0 !", 400)
        elif lookup(symbol) == None:                #해당 stock 존재하지 않으면 거름
            return apology("Stock doesn't exist!", 400)
        elif not cmpshares:                #로그인된 유저에게 해당 stock 없으면 거름, 없으면 cmpshares [] 임
            return apology("You don't have that!", 400)
        elif int(share) > cmpshares[0]["SUM(s_num)"]: #계속 이 좆같은 문제때문에 시간끌림 sqlite에서 가져왔는데 각 value 가 아니라 list형태로 있음 +
            return apology("It's more than you have!") #체크해보니까 얜 문제없는데 html input number에서 가져온 shares가 str형태로 있었음
                                                        # 확인해보려면 print(type()) 해보면 데이터타입알려줌
                                                        #print를 사용해서 문제파악하자 html input type number해도 str으로 저장됨

        else:
            shares = -abs(int(request.form.get("shares")))
            stockname = lookup(symbol)["name"]
            price = lookup(symbol)["price"]

            cash = db.execute("SELECT cash FROM users WHERE id = ?", user)[0]["cash"]
            cash = cash - (shares * price)
            # print(type(cmpshares[0]["SUM(s_num)"]))
            # print(type(shares))

            db.execute("INSERT INTO shares (user_id, s_name, s_num, price, total, symbol) VALUES(?,? , ?, ?, ?, ?)", user, stockname, shares, price, shares*price, stockname[0])
            db.execute("UPDATE users SET cash = ? WHERE id = ? ",cash ,user)
            return redirect("/")


    else:
        symbols = db.execute("SELECT symbol, SUM(s_num) FROM shares WHERE user_id = ? GROUP BY symbol ORDER BY symbol", user)
        return render_template("sell.html", symbols = symbols )
