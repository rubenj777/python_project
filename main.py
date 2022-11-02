import os
from flask import Flask, render_template, request, redirect, url_for, session


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    import db

    db.init_app(app)

    def get_id():
        id = session["id"]
        return id

    def get_role():
        role = session["role"]
        return role

    def who_am_i():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT * FROM app_user WHERE id=?", (get_id(),))
        me = res.fetchone()
        db.close_db()
        return me

    def get_all_users():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT * FROM app_user")
        users = res.fetchall()
        db.close_db()
        return users

    def get_all_appointments():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT * FROM appointment ")
        appointments = res.fetchall()
        db.close_db()
        return appointments


    def get_all_doctors():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT * FROM app_user WHERE role=2")
        doctors = res.fetchall()
        db.close_db()
        return doctors

    # def get_all_appointments():
    #     con = db.get_db()
    #     cur = con.cursor()
    #     res = cur.execute("SELECT visit.appointment_time, visit.cause, patient.username FROM visit INNER JOIN patient ON visit.id = patient.id WHERE id_1=? ORDER BY appointment_time DESC", (get_id()))
    #     visits = res.fetchall()
    #     db.close_db()
    #     return visits

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
            con = db.get_db()
            cur = con.cursor()
            res = cur.execute(
                "SELECT * FROM app_user WHERE username=? AND password=?",
                (username, password),
            )
            user = res.fetchone()

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
            # insert_visit()
            logged_user_id = get_id()
            doctors = get_all_doctors()
            appointments = get_all_appointments()
            users = get_all_users()
            return render_template(
                "home.html",
                users=users,
                appointments=appointments,
                doctors=doctors,
                logged_user_id=logged_user_id,
            )

    @app.route("/book", methods=["GET", "POST"])
    def book():
        doctor_id = request.form["doctor_id"]
        cause = request.form["cause"]
        datetime = request.form["datetime"]
        logged_user_id = request.form["logged_user_id"]
        con = db.get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO appointment ('user_id', 'doc_id', 'appointment_time', 'cause') VALUES (?, ?, ?, ?)", (logged_user_id, doctor_id, datetime, cause,)
        )
        con.commit()
        return redirect("/home")

    return app
