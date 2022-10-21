from ast import dump
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    import db

    db.init_app(app)

    def insert():
        con = db.get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO patient VALUES ('id', 'coucou', 'ruben', 'rub', 'password')"
        )
        con.commit()

    def get_all_patients():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT firstName, lastName, username FROM patient")
        lastName, firstName, username = res.fetchone()
        db.close_db()
        return firstName, lastName, username

   

    @app.route("/")
    def index():
        firstName, lastName, username = get_all_patients()

        return render_template(
            "index.html", firstName=firstName, lastName=lastName, username=username
        )

    return app
