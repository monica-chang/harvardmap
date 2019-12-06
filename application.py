# NOTE: Implemented HUID authentication using code from https://github.com/cs50/id/tree/master/flask
# TODO Get custom domain name using Github Student Pack https://www.name.com/partner/github-students

# ASK ABOUT HOW TO IMPORT ALL OF THIS
import os
import requests

from cs50 import SQL
from authlib.integrations.flask_client import OAuth
from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort, url_for
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology

# testing git

# Check for environment variables
for variable in ["CLIENT_ID", "CLIENT_SECRET", "SERVER_METADATA_URL"]:
    if not os.environ.get(variable):
        abort(500, f"Missing f{variable}")

# a different change

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure OAuth
oauth = OAuth(app)
oauth.register(
    "cs50",
    client_id=os.environ.get("CLIENT_ID"),
    client_kwargs={"scope": "openid profile email"},
    client_secret=os.environ.get("CLIENT_SECRET"),
    server_metadata_url=os.environ.get("SERVER_METADATA_URL")
)

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userinfo") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Configure CS50 Library to use SQLite database, will need tables for follower/followee + people at each location
db = SQL("sqlite:///harvardmap.db")

@app.route("/")
def index():
    return render_template("index.html", userinfo=session.get("userinfo"))

@app.route("/callback")
def callback():
    token = oauth.cs50.authorize_access_token()
    session["userinfo"] = oauth.cs50.parse_id_token(token)
    userinfo=session.get("userinfo")
    # if the user that just logged in has never logged in before, add the news user to the SQL database
    if len(db.execute("SELECT * FROM users WHERE sub=:sub", sub=userinfo["sub"])) == 0:
        newuser = db.execute("INSERT INTO users (sub, name, email) VALUES (:sub, :name, :email)", sub=userinfo["sub"], name=userinfo["name"], email=userinfo["email"])
    return redirect(url_for("index"))

@app.route("/login")
def login():
    return oauth.cs50.authorize_redirect(redirect_uri=url_for("callback", _external=True), userinfo=session.get("userinfo"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/map")
@login_required
def map():
    """Show interactive map of where students are on campus Note: potential harry potter theme!!!"""
    # Query for all relevant info for how many students are at each study spot

    return render_template("map2.html", userinfo=session.get("userinfo"))


@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    """Check the user into a study location"""

    userinfo=session.get("userinfo")

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Determine whether the user is checking in or out
        check = request.form.get("check")

        # Get the name of the location the user is checking in at
        location = request.form.get("location")
        if location == "First-Year Dorms":
            place = request.form.get("dorms")
        elif location == "Upperclassmen Houses":
            place = request.form.get("houses")
        elif location == "Libraries":
            place = request.form.get("libraries")
        elif location == "Cafes":
            place = request.form.get("cafes")
        else:
            place = request.form.get("location")

    #Ensure the place exists
    if place is None:
        return apology("must provide location")

    #Check the user in
    if check == "Check In":
        # Error check to make sure the user does not check into a location twice
        if db.execute("SELECT location FROM users WHERE :sub=sub", sub=userinfo["sub"]) == place:
            return apology("you have already checked in")
        else:
            # Update the user's current location in the database
            db.execute("UPDATE users SET location=:location WHERE sub=:sub", location=place, sub=userinfo["sub"])

            # If the location has not yet been checked into, add the location to the database
            if len(db.execute("SELECT * FROM locations WHERE location=:location", location=place)) == 0:
                db.execute("INSERT INTO locations (location, numpeople) VALUES (:location, :numpeople)", location=place, numpeople=0)
            # If the location has already been checked into, add 1 to the current number of people at the location
            else:
                db.execute("UPDATE locations SET numpeople = numpeople + 1 WHERE location=:location", location=place)

    # Check the user out
    else:
        # Error check to make sure the user does not check out of a location they haven't checked into yet
        if db.execute("SELECT location FROM users WHERE :sub=sub", sub=userinfo["sub"]) != place:
            return apology("you have not checked in yet")
        else:
            # Update the user's current location in the database
            db.execute("UPDATE users SET location=:location WHERE sub=:sub", location=NULL, sub=userinfo["sub"])
            # Subtract 1 from the current number of people at the location
            else:
                db.execute("UPDATE locations SET numpeople = numpeople - 1 WHERE location=:location", location=place)




            # insert the transaction into the database
            # update query to subtract 1 to user's location

            #return redirect("/confirm")

    #User reached route via GET, display form to request stock quote
    else:
        return render_template("check.html")


@app.route("/confirm")
@login_required
def confirm():
    """Confirm user successfully submitted request"""

    return render_template("confirm.html", userinfo=session.get("userinfo"))


@app.route("/friends", methods=["GET", "POST"])
@login_required
def friends():
    """Allow user to follow their friends and see their current location in a table"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username=request.form.get("username") # search for friend's username

        # Ensure username is entered
        if not username:
            return apology("must provide username", 403)
        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
            return apology("TODO")
        # Ensure username exists before following friend
        if len(rows) != 1:
            return apology("invalid username" , 403)
        else:
            return apology("TODO")
            #TODO update queries to establish follower/followee relationship

        return redirect("/friends")

    else:
        # query to get your friends and their current locations
        return render_template("friends.html", userinfo=session.get("userinfo"))


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
