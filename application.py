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
    # Create a list of locations
    locs = ['Smith Center', 'Apley Court', 'Canaday', 'Grays', 'Greenough', 'Hollis', 'Holworthy', 'Hurlbut', 'Lionel', 'Mower', 'Mass Hall', 'Matthews', 'Pennypacker', 'Stoughton', 'Straus', 'Thayer', 'Weld', 'Wigglesworth', 'Adams', 'Cabot', 'Currier', 'Dunster', 'Eliot', 'Kirkland', 'Leverett', 'Lowell', 'Mather', 'Pforzheimer', 'Quincy', 'Winthrop', 'Cabot', 'Langdell Law School Library','Lamont', 'Widener', 'Capital One', 'Flour', 'Peets', 'Starbucks', 'Tatte']
    # Create two dictionaries for numbers and names
    numbers = {}
    names = {}
    # For each location, add the number of people and names of people at each location to the respective dictionaries
    for loc in locs:
        numbers[loc]=db.execute("SELECT numpeople FROM locations WHERE location=:location", location=loc)[0]['numpeople']
        rows=db.execute("SELECT name FROM users WHERE location=:location", location=loc)
        names[loc]=[x['name'] for x in rows]

    print(numbers)
    print(names)

    return render_template("map2.html", userinfo=session.get("userinfo"), locs=locs, numbers=numbers, names=names)


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
        if location == "First-Year Dorm":
            place = request.form.get("dorms")
        elif location == "Upperclassmen House":
            place = request.form.get("houses")
        elif location == "Library":
            place = request.form.get("libraries")
        elif location == "Cafe":
            place = request.form.get("cafes")
        else:
            place = request.form.get("location")

        #Ensure the place exists
        if place is None:
            return apology("must provide location")

        #Check the user in
        if check == "Check In":
            # Error check to make sure the user does not check into a location twice
            if db.execute("SELECT location FROM users WHERE sub=:sub", sub=userinfo["sub"])[0]['location'] == place:
                return apology("you have already checked in")
            else:
                # Update the user's current location in the database
                db.execute("UPDATE users SET location=:location WHERE sub=:sub", location=place, sub=userinfo["sub"])

                # If the location has not yet been checked into, add the location to the database
                if len(db.execute("SELECT * FROM locations WHERE location=:location", location=place)) == 0:
                    db.execute("INSERT INTO locations (location, numpeople) VALUES (:location, :numpeople)", location=place, numpeople=1)
                # If the location has already been checked into, add 1 to the current number of people at the location
                else:
                    db.execute("UPDATE locations SET numpeople = numpeople + 1 WHERE location=:location", location=place)

                return redirect("/confirm")

        # Check the user out
        else:
            # Error check to make sure the user does not check out of a location they haven't checked into yet
            if db.execute("SELECT location FROM users WHERE sub=:sub", sub=userinfo["sub"])[0]['location'] != place:
                return apology("you have not checked in yet")
            # Error check to make sure there are not negative people at a location for some reason
            elif db.execute("SELECT numpeople FROM locations WHERE location=:location", location=place)[0]['numpeople'] <= 0:
                return apology("there cannot be negative people at this location")
            else:
                # Update the user's current location in the database
                db.execute("UPDATE users SET location=:location WHERE sub=:sub", location="Not checked in", sub=userinfo["sub"])
                # Subtract 1 from the current number of people at the location
                db.execute("UPDATE locations SET numpeople = numpeople - 1 WHERE location=:location", location=place)

                return redirect("/confirm")

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

    userinfo=session.get("userinfo")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email=request.form.get("email") # search for friend's email

        # Ensure email is entered
        if not email:
            return apology("must provide email", 403)
        else:
            # Query database for email
            rows = db.execute("SELECT * FROM users WHERE email=:email", email=email)

            # Ensure person exists before following them
            if len(rows) != 1:
                return apology("invalid email" , 403)

            # Query for the person's name
            name = db.execute("SELECT name FROM users WHERE email=:email", email=email)[0]['name']

            # Error check: if you already have 10 friends, you can't add anymore
            if (db.execute("SELECT COUNT(friend10) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend10)'] != 0):
                return apology ("You cannot follow more than 10 friends", 403)
            # If you have followed nine friends, add this user as your tenth friend (same logic applies to rest)
            elif (db.execute("SELECT COUNT(friend9) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend9)'] != 0):
                db.execute("UPDATE users SET friend10=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend8) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend8)'] != 0):
                db.execute("UPDATE users SET friend9=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend7) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend7)'] != 0):
                db.execute("UPDATE users SET friend8=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend6) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend6)'] != 0):
                db.execute("UPDATE users SET friend7=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend5) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend5)'] != 0):
                db.execute("UPDATE users SET friend6=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend4) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend4)'] != 0):
                db.execute("UPDATE users SET friend5=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend3) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend3)'] != 0):
                db.execute("UPDATE users SET friend4=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend2) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend2)'] != 0):
                db.execute("UPDATE users SET friend3=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            elif (db.execute("SELECT COUNT(friend1) FROM users WHERE sub=:sub", sub=userinfo['sub'])[0]['COUNT(friend1)'] != 0):
                db.execute("UPDATE users SET friend2=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

            else:
                db.execute("UPDATE users SET friend1=:name WHERE sub=:sub", name=name, sub=userinfo['sub'])

        return redirect("/friends")

    else:
        # query to get your friends and their current locations

        friend1=db.execute("SELECT friend1 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location1=db.execute("SELECT location FROM users WHERE name=:name", name=friend1[0]['friend1'])

        friend2=db.execute("SELECT friend2 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location2=db.execute("SELECT location FROM users WHERE name=:name", name=friend2[0]['friend2'])

        friend3=db.execute("SELECT friend3 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location3=db.execute("SELECT location FROM users WHERE name=:name", name=friend3[0]['friend3'])

        friend4=db.execute("SELECT friend4 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location4=db.execute("SELECT location FROM users WHERE name=:name", name=friend4[0]['friend4'])

        friend5=db.execute("SELECT friend5 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location5=db.execute("SELECT location FROM users WHERE name=:name", name=friend5[0]['friend5'])

        friend6=db.execute("SELECT friend6 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location6=db.execute("SELECT location FROM users WHERE name=:name", name=friend6[0]['friend6'])

        friend7=db.execute("SELECT friend7 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location7=db.execute("SELECT location FROM users WHERE name=:name", name=friend7[0]['friend7'])

        friend8=db.execute("SELECT friend8 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location8=db.execute("SELECT location FROM users WHERE name=:name", name=friend8[0]['friend8'])

        friend9=db.execute("SELECT friend9 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location9=db.execute("SELECT location FROM users WHERE name=:name", name=friend9[0]['friend9'])

        friend10=db.execute("SELECT friend10 FROM users WHERE sub=:sub", sub=userinfo['sub'])
        location10=db.execute("SELECT location FROM users WHERE name=:name", name=friend10[0]['friend10'])


        return render_template("friends.html", userinfo=session.get("userinfo"),
        friend1=friend1, location1=location1, friend2=friend2, location2=location2,
        friend3=friend3, location3=location3, friend4=friend4, location4=location4,
        friend5=friend5, location5=location5, friend6=friend6, location6=location6,
        friend7=friend7, location7=location7, friend8=friend8, location8=location8,
        friend9=friend9, location9=location9, friend10=friend10, location10=location10)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
