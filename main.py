from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    import db

    db.init_app(app)

    def insert_visit():
        con = db.get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO visit (id, id_1, 'appointment_time', 'cause') SELECT patient.id, doctor.id, '02/11/2022', 'foot hurt' FROM patient, doctor WHERE patient.id=2"
        )
        con.commit()

    def get_id():
        """cette fonction va servir à récupérer l'id du docteur connecté afin d'afficher seulement ses RDV dans la fonction get_all_appointments()"""
        """"pour l'instant il n'y a pas de fonction de connexion alors elle retourne 1"""
        return "1"

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
        res = cur.execute("SELECT visit.appointment_time, visit.cause, visit.id, visit.id_1, patient.username FROM visit INNER JOIN patient ON visit.id = patient.id WHERE id_1=? ORDER BY appointment_time DESC", (get_id()))
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
