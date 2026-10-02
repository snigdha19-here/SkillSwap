# ===================================================================
# frontend_preview.py  —  TEMPORARY FILE, DELETE ME LATER
# ===================================================================
# A tiny throw-away Flask app whose only job is to show the HTML pages
# with fake data, so the design can be checked before the real backend
# is finished.
#
# It does NOT import app.py, does NOT touch MongoDB and contains no real
# logic. Every POST route just shows a flash message and sends you back
# to the page you came from, which is exactly the shape the real backend
# will have: handle the form, then redirect.
#
# Run it with:      python frontend_preview.py
# Then open:        http://127.0.0.1:5001/
#
# It runs on port 5001 so it never clashes with the real app.py on 5000.
#
# Two preview-only tricks are built in, both added to the web address:
#   ?logged_out=1   pretend nobody is logged in (navbar shows Log in)
#   ?empty=1        pretend every list is empty (shows empty states)
# For example:      http://127.0.0.1:5001/sessions?empty=1
#
# Delete this file and mock_data.py once app.py serves the pages.
# ===================================================================

from flask import Flask, render_template, redirect, url_for, request, flash

# All the fake data lives in the other temporary file.
import mock_data


app = Flask(__name__)

# flash() needs a secret key to work. This one is fine because this app
# is only ever run on your own machine for a few minutes.
app.secret_key = "preview-only-not-a-real-secret"


# -------------------------------------------------------------------
# Two small helpers used by the page routes below.
# -------------------------------------------------------------------

def fake_user():
    """Return the pretend logged-in user, or None for ?logged_out=1."""
    if request.args.get("logged_out"):
        return None
    return mock_data.USER


def maybe_empty(real_list):
    """Return an empty list for ?empty=1, otherwise the sample list.

    This is how we look at both the full page and the friendly
    'nothing here yet' message without editing any files.
    """
    if request.args.get("empty"):
        return mock_data.EMPTY_LIST
    return real_list


# ===================================================================
# PAGES (GET)
# ===================================================================

@app.route("/")
def home():
    return render_template("home.html", user=fake_user())


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        flash("Preview only: your details were not saved.")
        return redirect(url_for("login"))
    # No user on purpose: somebody signing up is not logged in.
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("Preview only: pretending that worked.")
        return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("Preview only: you are 'logged out'.")
    return redirect(url_for("home", logged_out=1))


@app.route("/profile")
def profile():
    return render_template(
        "profile.html",
        user=fake_user(),
        teach_skills=maybe_empty(mock_data.TEACH_SKILLS),
        need_skills=maybe_empty(mock_data.NEED_SKILLS),
        topics=mock_data.TOPICS,
        languages=mock_data.LANGUAGES,
    )


@app.route("/ask", methods=["GET", "POST"])
def ask_help():
    if request.method == "POST":
        flash("Preview only: request not really sent. 1 credit would be spent.")
        return redirect(url_for("ask_help"))

    return render_template(
        "ask_help.html",
        user=fake_user(),
        topics=mock_data.TOPICS,
        languages=mock_data.LANGUAGES,
        my_requests=maybe_empty(mock_data.MY_REQUESTS),
    )


@app.route("/requests")
def incoming_requests():
    return render_template(
        "requests.html",
        user=fake_user(),
        requests_for_me=maybe_empty(mock_data.REQUESTS_FOR_ME),
    )


@app.route("/sessions")
def my_sessions():
    return render_template(
        "sessions.html",
        user=fake_user(),
        my_sessions=maybe_empty(mock_data.MY_SESSIONS),
    )


# ===================================================================
# FORM HANDLERS (POST only)
# Each one shows what was submitted as a flash message, then redirects.
# That is all a preview needs: it proves the form reaches the right
# address with the right field names.
# ===================================================================

@app.route("/profile/skills/add", methods=["POST"])
def add_skill():
    topic = request.form.get("topic")
    language = request.form.get("language")
    kind = request.form.get("kind")
    flash("Preview only: would add '%s' (%s) to your %s list."
          % (topic, language, kind))
    return redirect(url_for("profile"))


@app.route("/profile/skills/<skill_id>/delete", methods=["POST"])
def delete_skill(skill_id):
    flash("Preview only: would delete skill %s." % skill_id)
    return redirect(url_for("profile"))


@app.route("/profile/availability", methods=["POST"])
def toggle_availability():
    flash("Preview only: would flip your availability on or off.")
    return redirect(url_for("profile"))


@app.route("/requests/<request_id>/accept", methods=["POST"])
def accept_request(request_id):
    flash("Preview only: would accept request %s." % request_id)
    return redirect(url_for("incoming_requests"))


@app.route("/requests/<request_id>/decline", methods=["POST"])
def decline_request(request_id):
    flash("Preview only: would decline request %s." % request_id)
    return redirect(url_for("incoming_requests"))


@app.route("/sessions/<session_id>/done", methods=["POST"])
def finish_session(session_id):
    stars = request.form.get("stars")
    comment = request.form.get("comment")
    flash("Preview only: session %s would be done. Stars: %s. Comment: %s"
          % (session_id, stars, comment or "(none)"))
    return redirect(url_for("my_sessions"))


@app.route("/sessions/<session_id>/report", methods=["POST"])
def report_session(session_id):
    flash("Preview only: would report session %s." % session_id)
    return redirect(url_for("my_sessions"))


# ===================================================================
# Start the preview on port 5001.
# ===================================================================
if __name__ == "__main__":
    print("\n  SkillSwap frontend preview")
    print("  open http://127.0.0.1:5001/")
    print("  add ?logged_out=1 to any address to see the logged-out navbar")
    print("  add ?empty=1 to see the empty states")
    print("  press CTRL+C to stop\n")
    app.run(debug=True, port=5001)
