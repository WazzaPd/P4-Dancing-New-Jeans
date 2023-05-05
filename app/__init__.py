# Dancing New Jeans: David Chen, Joseph Wu, Nakib Abedin
# SoftDev
# Period 07
# Dec 2022
from flask import Flask  # facilitate flask webserving
from flask import render_template  # facilitate jinja templating
from flask import request  # facilitate form submission

app = Flask(__name__)  # create Flask object


@app.route("/", methods=['GET', 'POST'])
def display_homepage():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)  # displays app
    print("***DIAG: request obj ***")
    print(request)  # displays page request
    print("***DIAG: request.args ***")
    print(request.args)
    # print("***DIAG: request.args['username']  ***")
    # print(request.args['username'])
    print("***DIAG: request.headers ***")
    print(request.headers)
    return render_template('index.html')


@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.args ***")
    print(request.form)  # displays entered info as dict
    print("***DIAG: request.args['username']  ***")
    print(request.form['username'])
    print("***DIAG: request.headers ***")
    # metadata for the server about request+machine requesting
    print(request.headers)
    return f"Waaaa hooo HAAAH {request.form['username']}"  # response to a form submission


if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()