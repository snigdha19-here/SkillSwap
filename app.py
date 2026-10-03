# ---------------------------------------------------------------
# app.py: the "brain" of SkillSwap.
# This file runs the website: it shows pages, reads what users type,
# and saves things in our MongoDB database.
# ---------------------------------------------------------------

# --- Tools we borrow from other people's code (libraries) ---
import os                                  # lets us read settings from the computer
from dotenv import load_dotenv             # reads our secret settings from the .env file
from pymongo import MongoClient            # lets Python talk to MongoDB
from flask import Flask, render_template, request, redirect, url_for, flash,session                                 
from werkzeug.security import generate_password_hash, check_password_hash  # scrambles a password so we never store the real one
from bson import ObjectId
from functools import wraps

# --- Load our secret settings from the .env file ---
# .env holds MONGO_URI (the database address and password) and SECRET_KEY.
# It is NOT uploaded to GitHub, so our passwords stay private.
load_dotenv()

# --- Connect to the database ---
client = MongoClient(os.getenv("MONGO_URI"))   # open the connection to MongoDB Atlas
db = client["skillswap"]                       # our database is called "skillswap"
users = db["users"]                            # "users" is a collection (like a table) inside it
skills = db["skills"]                          # NEW: one document per skill a person can teach or needs

# --- Create the website itself ---
app = Flask(__name__)

# Flask needs a secret key to remember things about a visitor
# (like who is logged in) and to show flash messages.
app.secret_key = os.getenv("SECRET_KEY")

# Only emails ending with this can sign up. Change it to your college's ending.
COLLEGE_DOMAIN = "@heritageit.edu.in"

# The topics and languages people can choose from.
# We use fixed lists so "stack", "Stacks" and "stacks in c" never end up as different things.

TOPICS = ["Arrays", "Strings", "Pointers", "Linked lists", "Stacks", "Queues",
          "Recursion", "Trees", "Sorting", "Searching"]
LANGUAGES = ["C", "C++", "Python", "Java"]


# ---------------------------------------------------------------
# PAGES (called "routes"). Each @app.route line says:
# "when someone visits this web address, run the function below it".
# ---------------------------------------------------------------

# Home page: visiting "/" just shows home.html
@app.route("/")
def home():
    return render_template("home.html")


# Login page: GET shows the form, POST checks the email and password.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        found = users.find_one({"email": email})
        if found and check_password_hash(found["password_hash"], password):
            session["user_id"] = str(found["_id"])   # remember this person
            return redirect(url_for("profile"))

        flash("Wrong email or password.")
        return redirect(url_for("login"))
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


@app.route("/logout")
def logout():
    session.clear()          # forget who was logged in
    return redirect(url_for("home"))

# A "bouncer": put @login_required under a route to keep logged-out visitors out.
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:               # nobody logged in?
            flash("Please log in first.")
            return redirect(url_for("login"))      # send them to the login page
        return view(*args, **kwargs)               # logged in, so show the page normally
    return wrapped

#-----------------------------------------------------------------------------------------------------------------------------#

# --- TEMPORARY STUBS: real logic comes in later steps ---
def skills_for(user_id, kind):
    found = skills.find({"user_id": user_id, "kind": kind})
    # The page wants a text "id", but MongoDB's _id is a special object, so we convert it.
    return [{"id": str(s["_id"]), "topic": s["topic"], "language": s["language"]} for s in found]

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", teach_skills=[], need_skills=[], topics=TOPICS, languages=LANGUAGES)

@app.route("/profile/skills/add", methods=["POST"])
@login_required
def add_skill():
    topic = request.form["topic"]
    language = request.form["language"]
    kind = request.form["kind"]            # "teach" or "need"

    # Only accept values from our own lists, never trust what the browser sends.
    if topic not in TOPICS or language not in LANGUAGES or kind not in ("teach", "need"):
        flash("Please choose a topic and a language.")
        return redirect(url_for("profile"))

    # Don't allow the same skill twice.
    already = skills.find_one({"user_id": session["user_id"], "topic": topic,
                               "language": language, "kind": kind})
    if already:
        flash("You already added that.")
        return redirect(url_for("profile"))

    skills.insert_one({
        "user_id": session["user_id"],     # who this skill belongs to
        "topic": topic,
        "language": language,
        "kind": kind,
    })
    return redirect(url_for("profile"))

@app.route("/profile/skills/<skill_id>/delete", methods=["POST"])
def delete_skill(skill_id):
    return redirect(url_for("profile"))

@app.route("/profile/availability", methods=["POST"])
def toggle_availability():
    return redirect(url_for("profile"))

@app.route("/ask", methods=["GET", "POST"])
def ask_help():
    return render_template("ask_help.html", topics=[], languages=[], my_requests=[])

@app.route("/requests")
def incoming_requests():
    return render_template("requests.html", requests_for_me=[])

@app.route("/requests/<request_id>/accept", methods=["POST"])
def accept_request(request_id):
    return redirect(url_for("incoming_requests"))

@app.route("/requests/<request_id>/decline", methods=["POST"])
def decline_request(request_id):
    return redirect(url_for("incoming_requests"))

@app.route("/sessions")
def my_sessions():
    return render_template("sessions.html", my_sessions=[])

@app.route("/sessions/<session_id>/done", methods=["POST"])
def finish_session(session_id):
    return redirect(url_for("my_sessions"))

@app.route("/sessions/<session_id>/report", methods=["POST"])
def report_session(session_id):
    return redirect(url_for("my_sessions"))


# Runs before every page and adds a "user" variable to it,
# so templates can show the name, credits and rating in the navbar and profile.
@app.context_processor
def inject_user():
    user_id = session.get("user_id")          # who is logged in? (stored at login)
    if not user_id:
        return {}                             # nobody logged in, so no "user" variable
    u = users.find_one({"_id": ObjectId(user_id)})
    if not u:
        return {}
    count = u["rating_count"]
    avg = round(u["rating_sum"] / count, 1) if count else None   # average stars, or None if no ratings yet
    return {"user": {
        "name": u["name"],
        "email": u["email"],
        "credits": u["credits"],
        "avg_rating": avg,
        "available": u["available"],
    }}



# ---------------------------------------------------------------
# This starts the website when we run:  python app.py
# debug=True makes the page reload by itself when we change the code
# and shows helpful error messages. Turn it OFF before the real launch.
# ---------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)