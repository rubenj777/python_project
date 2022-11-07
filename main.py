from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    current_app,
)
from datetime import datetime
import sqlite3, click, os


def convert_datetime(val):
    return datetime.fromisoformat(val.decode())


def get_db():
    con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    sqlite3.register_converter("datetime", convert_datetime)
    con.row_factory = sqlite3.Row
    return con


def close_db(e=None):
    con = get_db()
    con.close()


def init_db():
    db = get_db()
    with current_app.open_resource("database.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    init_app(app)

    def date(d):
        return d.strftime("%A, %d. %B %Y %I:%M%p")

    app.add_template_filter(date)

    def get_now():
        now = datetime.now()
        return now

    def get_id():
        id = session["id"]
        return id

    def get_all_appointments():
        con = get_db()
        cur = con.cursor()
        if session["role"] == 2:
            res = cur.execute(
                "SELECT a.user_id, a.doc_id, a.appointment_time, a.cause, u.firstName, u.lastName, u.address, u.email, u.phone FROM appointment a INNER JOIN app_user u ON a.user_id = u.id ORDER BY a.appointment_time ASC"
            )
        if session["role"] == 1:
            res = cur.execute(
                "SELECT a.user_id, a.doc_id, a.appointment_time, a.cause, u.firstName, u.lastName, u.email, u.phone, u.specialization FROM appointment a INNER JOIN app_user u ON a.doc_id = u.id ORDER BY a.appointment_time ASC"
            )
        appointments = res.fetchall()
        now = get_now()
        close_db()
        return (
            appointments,
            now,
        )

    def get_all_doctors():
        con = get_db()
        cur = con.cursor()
        res = cur.execute("SELECT * FROM app_user WHERE role=2")
        doctors = res.fetchall()
        close_db()
        return doctors

    ###########################
    ######### ROUTES ##########
    ###########################

    @app.route("/")
    def index():
        if "loggedIn" not in session:
            return render_template("index.html")
        else:
            return redirect("/home")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            con = get_db()
            cur = con.cursor()
            res = cur.execute(
                "SELECT * FROM app_user WHERE username=? AND password=?",
                (username, password),
            )
            user = res.fetchone()
            close_db()

            if user:
                session["loggedIn"] = True
                session["id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                return redirect("/home")
            else:
                return redirect("/")

        return render_template("index.html")

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        session.pop("loggedIn", None)
        session.pop("id", None)
        session.pop("username", None)
        session.pop("role", None)
        return redirect("/")

    @app.route("/home")
    def home():
        if "loggedIn" not in session:
            return redirect("/")
        else:
            logged_user_id = get_id()
            doctors = get_all_doctors()
            appointments, now = get_all_appointments()
            my_id = get_id()
            return render_template(
                "home.html",
                appointments=appointments,
                now=now,
                doctors=doctors,
                logged_user_id=logged_user_id,
                my_id=my_id,
            )

    @app.route("/book", methods=["GET", "POST"])
    def book():
        doctor_id = request.form["doctor_id"]
        cause = request.form["cause"]
        datetime = request.form["datetime"]
        logged_user_id = request.form["logged_user_id"]
        con = get_db()
        cur = con.cursor()
        cur.execute(
            "REPLACE INTO appointment ('user_id', 'doc_id', 'appointment_time', 'cause') VALUES (?, ?, ?, ?)",
            (
                logged_user_id,
                doctor_id,
                datetime,
                cause,
            ),
        )
        con.commit()
        close_db()
        return redirect("/home")

    return app
