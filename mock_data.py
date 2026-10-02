# ===================================================================
# mock_data.py  —  TEMPORARY FILE, DELETE ME LATER
# ===================================================================
# This file holds fake sample data so the HTML pages can be looked at
# before the real Flask backend exists. It talks to no database and
# imports nothing from app.py.
#
# Every variable below is in EXACTLY the shape the templates expect, so
# it also works as a checklist: when your real backend passes these same
# shapes to render_template(), the pages will work unchanged.
#
# Delete this file and frontend_preview.py once app.py serves the pages.
# ===================================================================


# -------------------------------------------------------------------
# user  —  the person who is logged in.
# Every page may receive this. The navbar uses name and credits.
#   name       str   shown in the navbar and on the profile
#   email      str   shown on the profile
#   credits    int   how many sessions they can still ask for
#   avg_rating float or None   None means nobody has rated them yet
#   available  bool  True = currently free to help others
# -------------------------------------------------------------------
USER = {
    "name": "Riya Sharma",
    "email": "riya.sharma@heritageit.edu.in",
    "credits": 3,
    "avg_rating": 4.6,
    "available": True,
}

# The same shape, but for somebody who just signed up: 2 starting
# credits, no rating yet, and not marked available. Swap this into
# frontend_preview.py to check the "Not rated yet" and "Turn on" looks.
NEW_USER = {
    "name": "Arjun Das",
    "email": "arjun.das@heritageit.edu.in",
    "credits": 2,
    "avg_rating": None,
    "available": False,
}


# -------------------------------------------------------------------
# topics  —  a plain list of strings used to build every topic dropdown.
# profile.html and ask_help.html both receive this.
# -------------------------------------------------------------------
TOPICS = [
    "Pointers in C",
    "Recursion",
    "Linked Lists",
    "Big-O Notation",
    "SQL Joins",
    "Normalisation",
    "Git and GitHub",
    "Python Dictionaries",
    "Object Oriented Programming",
    "Matrices",
    "Probability",
    "Operating System Deadlocks",
]


# -------------------------------------------------------------------
# languages  —  a plain list of strings used to build every language
# dropdown. profile.html and ask_help.html both receive this.
# -------------------------------------------------------------------
LANGUAGES = [
    "English",
    "Hindi",
    "Bengali",
    "Tamil",
    "Telugu",
    "Marathi",
]


# -------------------------------------------------------------------
# teach_skills  —  topics this user can explain to others.
# Used by profile.html. Each item is {id, topic, language}.
#   id        str   whatever your backend uses to identify the skill.
#                   With MongoDB this will be str(skill["_id"]).
#   topic     str   one of the strings from TOPICS
#   language  str   one of the strings from LANGUAGES
# -------------------------------------------------------------------
TEACH_SKILLS = [
    {"id": "t1", "topic": "Pointers in C", "language": "English"},
    {"id": "t2", "topic": "Git and GitHub", "language": "Hindi"},
    {"id": "t3", "topic": "SQL Joins", "language": "Bengali"},
]


# -------------------------------------------------------------------
# need_skills  —  topics this user is stuck on.
# Used by profile.html. Same shape as TEACH_SKILLS.
# -------------------------------------------------------------------
NEED_SKILLS = [
    {"id": "n1", "topic": "Recursion", "language": "English"},
    {"id": "n2", "topic": "Probability", "language": "Hindi"},
]


# -------------------------------------------------------------------
# my_requests  —  help requests this user has sent out.
# Used by ask_help.html. Each item is {id, topic, language, status}.
#   status  str  must be one of: "waiting", "accepted", "declined", "done"
#                The status is what colours the badge, so all four are
#                listed here to check that all four colours look right.
# -------------------------------------------------------------------
MY_REQUESTS = [
    {"id": "r1", "topic": "Recursion",   "language": "English", "status": "waiting"},
    {"id": "r2", "topic": "Big-O Notation", "language": "Hindi", "status": "accepted"},
    {"id": "r3", "topic": "Matrices",    "language": "Bengali", "status": "declined"},
    {"id": "r4", "topic": "Normalisation", "language": "English", "status": "done"},
]


# -------------------------------------------------------------------
# requests_for_me  —  other students asking THIS user to teach them.
# Used by requests.html. Each item is {id, learner_name, topic, language}.
#   learner_name  str  the name of the person who needs help
# -------------------------------------------------------------------
REQUESTS_FOR_ME = [
    {
        "id": "q1",
        "learner_name": "Arjun Das",
        "topic": "Pointers in C",
        "language": "English",
    },
    {
        "id": "q2",
        "learner_name": "Meera Iyer",
        "topic": "Git and GitHub",
        "language": "Hindi",
    },
    {
        "id": "q3",
        "learner_name": "Sahil Khan",
        "topic": "SQL Joins",
        "language": "Bengali",
    },
]


# -------------------------------------------------------------------
# my_sessions  —  every session this user is part of.
# Used by sessions.html. Each item is:
#   id          str   identifies the session
#   role        str   "learner" (you are being taught) or
#                     "helper"  (you are teaching)
#   other_name  str   the other person's name
#   topic       str   what the session is about
#   language    str   which language it will be held in
#   status      str   "accepted" (arranged) or "done" (finished)
#   contact     str or None
#                     The contact details. Send None when this user is
#                     NOT allowed to see them. The template only writes
#                     this into the page when it is not None, so the
#                     server stays in charge of who sees what.
#   can_rate    bool  True = show the star form and "Mark as done"
#   stars       int or None   the rating already given, 1-5, or None
#
# The four entries below cover every combination worth looking at.
# -------------------------------------------------------------------
MY_SESSIONS = [
    {
        # Arranged, contact shared, waiting to be rated.
        "id": "s1",
        "role": "learner",
        "other_name": "Priya Nair",
        "topic": "Recursion",
        "language": "English",
        "status": "accepted",
        "contact": "priya.nair@heritageit.edu.in",
        "can_rate": True,
        "stars": None,
    },
    {
        # This user is the helper. Contact shared, rating not their job,
        # so can_rate is False.
        "id": "s2",
        "role": "helper",
        "other_name": "Arjun Das",
        "topic": "Pointers in C",
        "language": "English",
        "status": "accepted",
        "contact": "Phone: 98300 11223",
        "can_rate": False,
        "stars": None,
    },
    {
        # Finished and rated. Contact is no longer shared, so None.
        "id": "s3",
        "role": "learner",
        "other_name": "Meera Iyer",
        "topic": "SQL Joins",
        "language": "Hindi",
        "status": "done",
        "contact": None,
        "can_rate": False,
        "stars": 5,
    },
    {
        # Finished but nobody rated it: stars is None.
        "id": "s4",
        "role": "helper",
        "other_name": "Sahil Khan",
        "topic": "Git and GitHub",
        "language": "Bengali",
        "status": "done",
        "contact": None,
        "can_rate": False,
        "stars": None,
    },
]


# -------------------------------------------------------------------
# Empty versions, to check the "nothing here yet" messages.
# frontend_preview.py swaps these in when the web address ends with
# ?empty=1   for example  http://127.0.0.1:5001/requests?empty=1
# -------------------------------------------------------------------
EMPTY_LIST = []
