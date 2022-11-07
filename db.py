import sqlite3
import click
from flask import current_app


def get_db():
    con = sqlite3.connect("database.db")
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
