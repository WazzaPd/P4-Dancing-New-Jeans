import sqlite3
import os
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
