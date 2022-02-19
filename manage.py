from flask.cli import FlaskGroup
import app

cli = FlaskGroup(app.create_app())

@cli.command("create_db")
def create_db():
    app.db.create_all()
    app.db.session.commit()

@cli.command("hello")
def hello():
    print("Hello")

if __name__ == "__main__":
    cli()
