# Dancing New Jeans: David Chen, Joseph Wu, Nakib Abedin
# SoftDev
# Period 08
# Dec 2023

import sqlite3  # for database building
from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request  # facilitate form submission
from flask import session  # facilitate user sessions
from flask import redirect, url_for  # to redirect to a different URL
import os

app = Flask(__name__)  # create Flask object
# randomized string for SECRET KEY (for interacting with operating system)
app.secret_key = os.urandom(32)

DB_FILE = "tables.db"
# open if file exists, otherwise create
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()  # facilitate db ops -- you will use cursor to trigger db events

c.execute("create table if not exists accounts(email TEXT, password TEXT);")
db.commit()


@app.route("/", methods=['GET', 'POST'])
def index():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)  # displays app
    print("***DIAG: request obj ***")
    print(request)  # displays page request
    print("***DIAG: request.args ***")
    print(request.args)
    # print("***DIAG: request.args['email']  ***")
    # print(request.args['email'])
    print("***DIAG: request.headers ***")
    print(request.headers)

    if 'email' in session:
        print("user is logged in as " +
              session['email'] + ". Redirecting to /")
        return render_template('index.html', email = True)
    return render_template('index.html', email = False)

# REGISTER


@app.route("/register", methods=['GET', 'POST'])
def register():

    # GET
    if request.method == 'GET':
        return render_template('register.html')

    # POST
    if request.method == 'POST':
        input_email = request.form['email']
        input_password = request.form['password']
        input_confirm_password = request.form['confirm password']

    # if no registration info is inputted into the fields
    if input_email.strip() == '' or input_password.strip() == '' or input_confirm_password.strip() == '':
        error_msg = ""
        if input_email == '':
            error_msg += "Please enter a email. \n"

        if input_password == '':
            error_msg += "Please enter a password. \n"

        if input_confirm_password == '':
            error_msg += "Please confirm your password. \n"

        return render_template('register.html', message=error_msg)

    # if info is entered into fields
    else:
        # Checks for password/confirm password match
        if input_password != input_confirm_password:
            return render_template('register.html', message="Passwords do not match. Please try again.")

        # Checks for existing email in accounts table
        var = (input_email,)
        c.execute("select email from accounts where email=?", var)

        # if there isn't an account associated with said email then create one
        if not c.fetchone():
            c.execute("insert into accounts values(?, ?)",
                      (input_email, input_password))
            return render_template('login.html')
        # if email is already taken
        else:
            return render_template('register.html', message="email is already taken. Please select another email.")

# login process


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Already logged in
    if 'email' in session:
        print("user is logged in as " +
              session['email'] + " is already logged in. Redirecting to /")
        return redirect("/")

    # GET
    if request.method == "GET":
        return render_template("login.html")

    # POST
    if request.method == 'POST':
        input_email = request.form['email']
        input_password = request.form['password']

    # Searches accounts table for user-password combination
    c.execute("select email from accounts where email=? and password=?;",
              (input_email, input_password))

    # login_check
    if c.fetchone():
        print("Login success!")
        if request.method == 'GET':  # For 'get'
            # stores email in session
            session['email'] = request.args['email']

        if request.method == 'POST':  # For 'post'
            # stores email in session
            session['email'] = request.form['email']

        return redirect("/")

    else:
        print("Login failed")
        error_msg = ''
        email_check = "select email from accounts where email=?;"
        password_check = "select email from accounts where password=?;"

        # email check
        c.execute(email_check, (input_email,))
        if not c.fetchone():
            error_msg += "email is incorrect or not found. \n"

        # Password check
        c.execute(password_check, (input_password,))
        if not c.fetchone():
            error_msg += "Password is incorrect or not found. \n"

        error_msg += "Please try again."
        return render_template('login.html', message=error_msg)

# logout and redirect to login page


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # remove the email from the session if it's there
    session.pop('email', None)
    print("user has logged out. Redirecting to /login")
    return redirect("/")

# @app.route("/auth", methods=['GET', 'POST'])
# def authenticate():
#     print("\n\n\n")
#     print("***DIAG: this Flask obj ***")
#     print(app)
#     print("***DIAG: request obj ***")
#     print(request)
#     print("***DIAG: request.args ***")
#     print(request.form)  # displays entered info as dict
#     print("***DIAG: request.args['email']  ***")
#     print(request.form['email'])
#     print("***DIAG: request.headers ***")
#     # metadata for the server about request+machine requesting
#     print(request.headers)
#     return f"Waaaa hooo HAAAH {request.form['email']}"  # response to a form submission


# @app.route("/index", methods=['GET', 'POST'])
# def main():
#     if 'email' in session:
#         return render_template('index.html')
#     else:
#         print("user is not logged in. Redirecting to /login")
#         return redirect("/login")


@app.route("/buy", methods=['GET', 'POST'])
def buy():
    if 'email' in session:
        return render_template('buy.html', email = True)
    return render_template('buy.html', email = False)
    


@app.route("/rent", methods=['GET', 'POST'])
def rent():
    if 'email' in session:
        return render_template('rent.html', email = True)
    return render_template('rent.html', email = False)

@app.route("/sell", methods=['GET', 'POST'])
def sell():
    if 'email' in session:
        return render_template('sell.html', email = True)
    return render_template('sell.html', email = False)


if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
