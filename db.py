import sqlite3
import click
from flask import current_app


def get_db():
    con = sqlite3.connect("database.db")
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
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# cur.execute("CREATE TABLE if not exists patient(id, firstName, lastName, username, PRIMARY KEY(id))")
# cur.execute("CREATE TABLE if not exists doctor(id, firstName, lastName, username, specialisation, PRIMARY KEY(id))")

# cur.execute("drop table if exists patient")
# cur.execute("drop table if exists doctor")
# cur.execute("drop table if exists visit")
