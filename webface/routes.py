from . import app
from flask import render_template, request, redirect, url_for, session, flash
import functools
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
dbfile="databaze.sqlite"
conn=sqlite3.connect("databaze.sqlite", isolation_level=None)

# from werkzeug.security import check_password_hash

slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html.j2")


@app.route("/login/")
def login():
    return render_template("login.html.j2")


@app.route("/login/", methods=["POST"])
def login_post():
    nick = request.form.get("nick")
    passwd = request.form.get("passwd")
    if nick and passwd:
        with sqlite3.connect(dbfile) as conn:
            tabulka =list(conn.execute("SELECT passwd FROM uzivatel WHERE nick=?", [nick]))
            print(tabulka)
        if tabulka and check_password_hash(tabulka[0][0], passwd):
            flash("Ano!")
        else:
            flash("Ne!")
    return redirect(url_for("index"))


@app.route("/register/")
def register():
    return render_template("register.html.j2", slova=slova)


@app.route("/register/", methods=["POST"])
def register_post():
    nick = request.form.get("nick")
    passwd1 = request.form.get("passwd1")
    passwd2 = request.form.get("passwd2")
    if nick and passwd1 and passwd2 == passwd1:
        hashpasswd = generate_password_hash('passwd1')
        with sqlite3.connect(dbfile) as conn:
            try:
                conn.execute("INSERT INTO uzivatel (nick,passwd) VALUES (?,?)", [nick, hashpasswd])
                flash("Uživatel vytvořen!")
            except sqlite3.IntegrityError:
                flash("Uživatel již existuje!")
    else:
        flash("Chyba: je nutné zadat správně veškeré údaje!")
        return redirect(url_for("register"))
    return redirect(url_for("index"))


@app.route("/text/")
def text():
    return """

<h1>Text</h1>

<p>toto je text</p>

"""
