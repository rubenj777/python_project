from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    import db

    db.init_app(app)

    def insert_visit():
        con = db.get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO visit (id, id_1, 'appointment_time', 'cause') SELECT patient.id, doctor.id, '2003/01/22', 'foot hurt' FROM patient, doctor"
        )
        con.commit()

    def get_all_patients():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT firstName, lastName, email, phone FROM patient")
        patients = res.fetchall()
        db.close_db()
        return patients

    def get_all_doctors():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT username, specialization FROM doctor")
        doctors = res.fetchall()
        db.close_db()
        return doctors

    def get_all_appointments():
        con = db.get_db()
        cur = con.cursor()
        res = cur.execute("SELECT appointment_time, cause, id, id_1 FROM visit")
        visits = res.fetchall()
        db.close_db()
        return visits

    @app.route("/home")
    def index():
        #insert_visit()
        visits = get_all_appointments()
        patients = get_all_patients()
        doctors = get_all_doctors()
        return render_template("home.html", patients=patients, visits=visits, doctors=doctors)

    return app
