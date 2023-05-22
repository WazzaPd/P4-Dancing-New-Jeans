# Dancing New Jeans: David Chen, Joseph Wu, Nakib Abedin
# SoftDev
# Period 08
# Dec 2023

# import sqlite3  # for database building
from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request  # facilitate form submission
from flask import session  # facilitate user sessions
from flask import redirect, url_for, jsonify  # to redirect to a different URL
import os
import requests
from db import *

dirname = os.path.dirname(__file__)
attomKey = open(os.path.join(dirname, "keys/attom.txt")
                ).read() or ""


app = Flask(__name__)  # create Flask object
# randomized string for SECRET KEY (for interacting with operating system)
app.secret_key = os.urandom(32)

# DB_FILE = os.path.join(dirname, "tables.db")
# db = sqlite3.connect(DB_FILE, check_same_thread=False)
# c = db.cursor()
# # open if file exists, otherwise create
# db = sqlite3.connect(DB_FILE, check_same_thread=False)
# c = db.cursor()  # facilitate db ops -- you will use cursor to trigger db events

# c.execute("create table if not exists accounts(email TEXT, password TEXT);")
# db.commit()


def render_template(template, **kwargs):
    email = session.get('email', None)
    print("email is " + str(email) + " in render_template_with_username")
    return render_template(template, email=email, **kwargs)


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
        return render_template('index.html')
    return render_template('index.html')

# REGISTER


@app.route("/register", methods=['POST'])
def register():

    # POST
    if request.method == 'POST':
        input_email = request.form['email']
        input_password = request.form['password']
        confirm_password = request.form['confirm_password']

        response = {
            'error': '',
            'success': ''
        }
        # if no registration info is inputted into the fields
        if input_email.strip() == '' or input_password.strip() == '' or confirm_password.strip() == '':
            # return json response instead of rendering template
            if input_email.strip() == '':
                response['error'] = "Please enter a email. \n"

            if input_password.strip() == '':
                response['error'] += "Please enter a password. \n"

            if confirm_password.strip() == '':
                response['error'] += "Please confirm your password. \n"

            if input_password.strip() != confirm_password.strip():
                response['error'] += "Passwords do not match. \n"

            response['success'] = "false"
            return jsonify(response)

            # if info is entered into fields
        else:
            # Checks for existing email in accounts table
            # var = (input_email,)
            # c.execute("select email from accounts where email=?", var)\

            if check_email(input_email):
                response['error'] = "email is already taken. Please select another email. \n"
                response['success'] = "false"
                return jsonify(response)

            # if email is not taken
            else:
                # if passwords match
                if input_password == confirm_password:
                    # insert into accounts table
                    insert_account(input_email, input_password)
                    response['success'] = "true"
                    return jsonify(response)
                # if passwords don't match
                else:
                    response['error'] = "Passwords do not match. \n"
                    response['success'] = "false"
                    return jsonify(response)
    else:
        # return status code 405 (method not allowed)
        return 405
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
    c.execute("select email from users where email=? and password=?;",
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
    ip_data = get_ip_data(get_ip())
    # print(data)
    zip = ip_data['zip']
    print(zip)

    data = homes_by_zip(zip)
    print(data)
    return render_template('buy.html', query=zip, data=data['property'])


def get_ip():
    # if the addr is 127.0.0.1 then request for the ip
    if request.remote_addr == "127.0.0.1":
        ip = requests.get("https://api.ipify.org").text
    else:
        ip = request.remote_addr
    return ip


def get_ip_data(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    print(data)
    return data


@app.route("/search", methods=['GET', 'POST'])
def search():
    if 'email' in session:
        return render_template('search.html')
    return render_template('search.html')


@app.route("/rent", methods=['GET', 'POST'])
def rent():
    if 'email' in session:
        return render_template('rent.html', email=True)
    return render_template('rent.html')


@app.route("/sell", methods=['GET', 'POST'])
def sell():
    if 'email' in session:
        return render_template('sell.html', email=True)
    return render_template('sell.html', email=False)

# proxy api routes for attom property api


# @app.route("/api/property/address", methods=['GET'])
def homes_by_zip(zip):
    # fetch data and return json
    headers = {
        'Accept': 'application/json, application/json',
        'apikey': attomKey,
    }

    # required params
    # if 'zip' not in request.args:
    #     return {'error': 'missing required parameter: zip'}

    params = {
        'postalcode': zip,
        'page': '1',
        'pagesize': '100',
    }

    response = requests.get(
        'https://api.gateway.attomdata.com/propertyapi/v1.0.0/assessment/detail', params=params, headers=headers)
    return response.json()


if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
