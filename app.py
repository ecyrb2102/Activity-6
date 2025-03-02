from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_hashing import Hashing
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sample.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

bootstrap = Bootstrap(app)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

hashing = Hashing(app)

class Profile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def __repr__(self):
        return self.username

    def hash_pass(password):
        return hashing.hash_value(password, salt="abcd")

@app.route("/")
def home():
    profiles = Profile.query.all()
    return render_template("home.html", profiles=profiles)

@app.route("/view/<int:id>")
def read(id):
    profile = Profile.query.get(id)
    return render_template("read.html", profile=profile)

@app.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        password = request.form["password"]
        profile = Profile(firstname=firstname,
                        lastname=lastname,
                        username=username,
                        password=Profile.hash_pass(password))
        db.session.add(profile)
        db.session.commit()
        flash(f"{username} added successfully")
    return render_template("create.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def update(id):
    profile = Profile.query.get(id)
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        profile.firstname = firstname
        profile.lastname = lastname
        db.session.commit()
        flash(f"{profile.username} editted successfully")
    return render_template("update.html", profile=profile)

@app.route("/delete/<int:id>")
def remove(id):
    Profile.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f"Deleted successfully")
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

