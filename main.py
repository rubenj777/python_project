from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    import db

    db.init_app(app)

    def insert():
        con = db.get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO patient (firstName, lastName, username, password, address, email, phone) VALUES ('mohamed', 'konate', 'moko', 'password', 'lyon', 'mohamed@mail.com', '0656980564')"
        )
        con.commit()

    def get_all_patients():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT firstName, lastName, email, phone FROM patient")
        patients = res.fetchall()
        db.close_db()
        return patients

    @app.route("/home")
    def index():
        #insert()
        patients = get_all_patients()
        return render_template("home.html", patients=patients)

    return app
