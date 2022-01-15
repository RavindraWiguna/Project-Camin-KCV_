from os import name
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<address>/")
def any(address):
    return render_template("index.html", isi=address)

if __name__ == "__main__":
    app.run(debug=True)

