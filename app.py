# ---------------------------------------------------------------
# app.py: the "brain" of SkillSwap.
# This file runs the website: it shows pages, reads what users type,
# and saves things in our MongoDB database.
# ---------------------------------------------------------------

# --- Tools we borrow from other people's code (libraries) ---
import os                                  # lets us read settings from the computer
from dotenv import load_dotenv             # reads our secret settings from the .env file
from pymongo import MongoClient            # lets Python talk to MongoDB
from flask import (                        # Flask = the tool that builds the website
    Flask,
    render_template,                       # shows an HTML page
    request,                               # holds what the user typed in a form
    redirect,                              # sends the user to a different page
    url_for,                               # finds the web address of a page by its function name
    flash,                                 # shows a short message like "Wrong email"
)
from werkzeug.security import generate_password_hash   # scrambles a password so we never store the real one

# --- Load our secret settings from the .env file ---
# .env holds MONGO_URI (the database address and password) and SECRET_KEY.
# It is NOT uploaded to GitHub, so our passwords stay private.
load_dotenv()

# --- Connect to the database ---
client = MongoClient(os.getenv("MONGO_URI"))   # open the connection to MongoDB Atlas
db = client["skillswap"]                       # our database is called "skillswap"
users = db["users"]                            # "users" is a collection (like a table) inside it

# --- Create the website itself ---
app = Flask(__name__)

# Flask needs a secret key to remember things about a visitor
# (like who is logged in) and to show flash messages.
app.secret_key = os.getenv("SECRET_KEY")

# Only emails ending with this can sign up. Change it to your college's ending.
COLLEGE_DOMAIN = "@heritageit.edu.in"


# ---------------------------------------------------------------
# PAGES (called "routes"). Each @app.route line says:
# "when someone visits this web address, run the function below it".
# ---------------------------------------------------------------

# Home page: visiting "/" just shows home.html
@app.route("/")
def home():
    return render_template("home.html")


# Login page: for now it only shows the page. We add the login logic in Step 2c.
@app.route("/login")
def login():
    return render_template("login.html")


# Sign-up page.
# GET  = the user just opened the page, so we show the empty form.
# POST = the user pressed the "Sign up" button, so we process what they typed.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # 1. Read what the user typed into the form.
        #    The names "name", "email", "password" must match the
        #    name="..." parts of the inputs in signup.html.
        name = request.form["name"].strip()            # .strip() removes extra spaces
        email = request.form["email"].strip().lower()  # .lower() so A@x.com and a@x.com count as the same
        password = request.form["password"]

        # 2. Only college emails are allowed.
        if not email.endswith(COLLEGE_DOMAIN):
            flash("Please use your college email.")    # message shown on the page
            return redirect(url_for("signup"))         # send them back to the form

        # 3. Stop people from signing up twice with the same email.
        if users.find_one({"email": email}):           # search the database for this email
            flash("This email is already registered.")
            return redirect(url_for("signup"))

        # 4. Everything is fine, so save the new user in the database.
        users.insert_one({
            "name": name,
            "email": email,
            "password_hash": generate_password_hash(password),  # scrambled password, never the real one
            "credits": 2,          # every new user starts with 2 free credits
            "rating_sum": 0,       # total stars received so far (used to work out the average later)
            "rating_count": 0,     # how many ratings received so far
            "available": True,     # True = free to help others right now
        })

        # 5. Account created, so send them to the login page.
        return redirect(url_for("login"))

    # If we reach here, the user only opened the page (GET), so show the form.
    return render_template("signup.html")



# ---------------------------------------------------------------
# This starts the website when we run:  python app.py
# debug=True makes the page reload by itself when we change the code
# and shows helpful error messages. Turn it OFF before the real launch.
# ---------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)