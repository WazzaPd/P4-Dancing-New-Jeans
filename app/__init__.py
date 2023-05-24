# Dancing New Jeans: David Chen, Joseph Wu, Nakib Abedin
# SoftDev
# Period 08
# Dec 2023

# import sqlite3  # for database building
import sqlite3
import base64
from PIL import Image, ImageDraw
import random
from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request  # facilitate form submission
from flask import session  # facilitate user sessions
from flask import redirect, url_for, jsonify  # to redirect to a different URL
import os
import requests
# # from .database import *
# from art import *

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


def render_template_with_email(template, **kwargs):
    emailStr = session.get('email', None)
    print("email is " + str(emailStr) + " in render_template_with_email")
    return render_template(template, email=emailStr, **kwargs)


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

    return render_template_with_email('index.html')

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
            # return render_template_with_email('register.html', message=response['error'])
            # return home page with url params
            return redirect(f"/?error={response['error']}&modal=register")

            # if info is entered into fields
        else:
            # Checks for existing email in accounts table
            # var = (input_email,)
            # c.execute("select email from accounts where email=?", var)\

            if check_email(input_email):
                response['error'] = "email is already taken. Please select another email. \n"
                response['success'] = "false"
                return redirect(f"/?error={response['error']}&modal=register")

            # if email is not taken
            else:
                # if passwords match
                if input_password == confirm_password:
                    # insert into accounts table
                    insert_account(input_email, input_password)
                    response['success'] = "true"
                    return redirect(f"/?success=Successfully registered!&modal=register")
                # if passwords don't match
                else:
                    response['error'] = "Passwords do not match. \n"
                    response['success'] = "false"
                    print("Passwords do not match")
                    return redirect(f"/?error={response['error']}&modal=register")
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
        return render_template_with_email("login.html")

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
        return render_template_with_email('login.html', message=error_msg)

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
#         return render_template_with_email('index.html')
#     else:
#         print("user is not logged in. Redirecting to /login")
#         return redirect("/login")

# function to return a specified amount of randomly generated image buffers
def gen_house_buffers(amount):
    buffers = []
    # call generate_house to get a random house image buffer
    for i in range(amount):
        buffers.append(generate_house())
    return buffers


@app.route("/search", methods=['GET'])
def search():
    # print all the url params in kv pairs
    for key, value in request.args.items():
        print(f"{key}: {value}")

    zip = request.args['postalCode']
    data = homes_by_zip(zip)
    print(data)
    # if 'email' in session:
    #     return render_template_with_email('search.html')
    return render_template_with_email('buy.html', query=zip, data=data['property'], pixelart=gen_house_buffers(len(data['property'])))


@app.route("/buy", methods=['GET', 'POST'])
def buy():
    ip_data = get_ip_data(get_ip())
    # print(data)
    zip = ip_data['zip']
    print(zip)

    data = homes_by_zip(zip)
    print(data)

    return render_template_with_email('buy.html', query=zip, data=data['property'], pixelart=gen_house_buffers(len(data['property'])))


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


@ app.route("/rent", methods=['GET', 'POST'])
def rent():
    if 'email' in session:
        return render_template_with_email('rent.html')
    return render_template_with_email('rent.html')


@ app.route("/sell", methods=['GET', 'POST'])
def sell():
    if 'email' in session:
        return render_template_with_email('sell.html')
    return render_template_with_email('sell.html')

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
        'pagesize': '30',
    }

    response = requests.get(
        'https://api.gateway.attomdata.com/propertyapi/v1.0.0/assessment/detail', params=params, headers=headers)
    return response.json()


@app.route("/api/property/address", methods=['GET'])
def expanded_detail_home():
    # fetch data and return json
    headers = {
        'Accept': 'application/json, application/json',
        'apikey': attomKey,
    }

    attomId = request.args['id']
    # required params
    # if 'zip' not in request.args:
    #     return {'error': 'missing required parameter: zip'}

    params = {
        'id': attomId,
        # 'page': '1',
        # 'pagesize': '100',
    }

    response = requests.get(
        'https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/expandedprofile', params=params, headers=headers)
    # return response.json()
    data = response.json()['property'][0]
    return data

# import os


dirname = os.path.dirname(__file__)

DB_FILE = os.path.join(dirname, "tables.db")

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()  # facilitate db ops -- you will use cursor to trigger db events

# three tables: users, orders in cart, order history
c.execute(
    "CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, password TEXT)")
# execute with relation to users table
c.execute(
    "CREATE TABLE IF NOT EXISTS order_history(email TEXT PRIMARY KEY, cart, history)")

c.execute("CREATE TABLE IF NOT EXISTS orders(email TEXT, productName TEXT, date TEXT, quantity INT, productSKU TEXT, productPrice REAL, orderID INT PRIMARY KEY)")
# TODO work this out later

# c.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, SKU TEXT, name TEXT, price REAL, description TEXT, image TEXT)")

db.commit()  # save changes


def check_email(email):
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    if c.fetchone():
        return True
    else:
        return False


def insert_account(email, password):
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
              (email, password))
    db.commit()


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_house():
    width, height = 256, 256
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Draw a random building type
    building_type = random.choice(["house", "apartment", "cabin", "mansion"])

    if building_type == "house":
        # draw windows
        draw.rectangle([(64, 128), (192, 240)], fill=random_color())
        draw.polygon([(64, 128), (192, 128), (128, 64)], fill=random_color())
        # draw doors and chimney
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())
        draw.rectangle([(128, 64), (160, 96)], fill=random_color())
    elif building_type == "apartment":

        # draw windows
        draw.rectangle([(64, 64), (192, 240)], fill=random_color())
        for i in range(3):
            draw.rectangle(
                [(80, 80 + 48 * i), (176, 112 + 48 * i)], fill=random_color())
        # draw doors
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())

    elif building_type == "cabin":

        # draw windows
        draw.rectangle([(64, 128), (192, 240)], fill=random_color())
        draw.rectangle([(64, 64), (96, 96)], fill=random_color())
        draw.rectangle([(160, 64), (192, 96)], fill=random_color())
        # draw doors
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())
        draw.rectangle([(128, 64), (160, 96)], fill=random_color())

    elif building_type == "mansion":

        # draw windows
        draw.rectangle([(64, 64), (192, 240)], fill=random_color())
        for i in range(3):
            draw.rectangle(
                [(80, 80 + 48 * i), (176, 112 + 48 * i)], fill=random_color())
        # draw doors
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())
        draw.rectangle([(128, 64), (160, 96)], fill=random_color())
        # draw roof
        draw.polygon([(64, 64), (192, 64), (128, 32)], fill=random_color())

    # convert pil image to base64
    # save image to temp file and get base64
    image.save("temp.png")
    with open("temp.png", "rb") as image_file:
        # get base 64
        encoded_string = base64.b64encode(image_file.read())
        # print(encoded_string)
        # remove temp file
        # print(encoded_string)
        # remove b prefix and quotes
        encoded_string = str(encoded_string)[2:-1]
        return encoded_string


# # Generate and show a random house
house_image = generate_house()
# house_image.show()


if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
