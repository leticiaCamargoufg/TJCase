from flask import render_template
from app import app

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/casos")
def casos():
    return render_template("caso.html")