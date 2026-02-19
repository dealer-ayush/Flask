from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "abc"
ADMIN_CODE = "COLLEGE123"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    message = db.Column(db.String(200))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.String(50))
    location = db.Column(db.String(100))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    link = db.Column(db.String(200))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":

        role = request.form["role"]
        admin_code = request.form.get("admin_code")

        if role == "admin" and admin_code != ADMIN_CODE:
            return "Invalid Admin Code!"

        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"],
            password=request.form["password"]
        ).first()

        if user:
            session["user"] = user.name
            session["role"] = user.role
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/users")
def users():
    if session.get("role") != "admin":
        return redirect("/dashboard")

    data = User.query.all()
    return render_template("users.html", data=data)

@app.route("/delete_user/<int:id>")
def delete_user(id):
    if session.get("role") != "admin":
        return redirect("/dashboard")

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    notes = Note.query.all()   
    return render_template("dashboard.html",
                           name=session["user"],
                           role=session["role"],
                           notes=notes)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/announcements")
def announcements():
    data = Announcement.query.all()
    return render_template("announcements.html", data=data, role=session.get("role"))

@app.route("/add_announcement", methods=["POST"])
def add_announcement():
    if session.get("role") != "admin":
        return redirect("/announcements")
    a = Announcement(title=request.form["title"], message=request.form["message"])
    db.session.add(a)
    db.session.commit()
    return redirect("/announcements")

@app.route("/delete_announcement/<int:id>")
def delete_announcement(id):
    if session.get("role") != "admin":
        return redirect("/announcements")
    db.session.delete(Announcement.query.get(id))
    db.session.commit()
    return redirect("/announcements")

@app.route("/edit_announcement/<int:id>")
def edit_announcement(id):
    data = Announcement.query.all()
    edit = Announcement.query.get(id)
    return render_template("announcements.html", data=data, edit=edit, role=session.get("role"))

@app.route("/update_announcement/<int:id>", methods=["POST"])
def update_announcement(id):
    a = Announcement.query.get(id)
    a.title = request.form["title"]
    a.message = request.form["message"]
    db.session.commit()
    return redirect("/announcements")


@app.route("/events")
def events():
    data = Event.query.all()
    return render_template("events.html", data=data, role=session.get("role"))

@app.route("/add_event", methods=["POST"])
def add_event():
    if session.get("role") != "admin":
        return redirect("/events")
    e = Event(title=request.form["title"], date=request.form["date"], location=request.form["location"])
    db.session.add(e)
    db.session.commit()
    return redirect("/events")

@app.route("/delete_event/<int:id>")
def delete_event(id):
    if session.get("role") != "admin":
        return redirect("/events")
    db.session.delete(Event.query.get(id))
    db.session.commit()
    return redirect("/events")

@app.route("/edit_event/<int:id>")
def edit_event(id):
    data = Event.query.all()
    edit = Event.query.get(id)
    return render_template("events.html", data=data, edit=edit, role=session.get("role"))

@app.route("/update_event/<int:id>", methods=["POST"])
def update_event(id):
    e = Event.query.get(id)
    e.title = request.form["title"]
    e.date = request.form["date"]
    e.location = request.form["location"]
    db.session.commit()
    return redirect("/events")


@app.route("/notes")
def notes():
    data = Note.query.all()
    return render_template("notes.html", data=data, role=session.get("role"))

@app.route("/add_note", methods=["POST"])
def add_note():
    if session.get("role") != "admin":
        return redirect("/notes")
    n = Note(subject=request.form["subject"], link=request.form["link"])
    db.session.add(n)
    db.session.commit()
    return redirect("/notes")

@app.route("/delete_note/<int:id>")
def delete_note(id):
    if session.get("role") != "admin":
        return redirect("/notes")
    db.session.delete(Note.query.get(id))
    db.session.commit()
    return redirect("/notes")

@app.route("/edit_note/<int:id>")
def edit_note(id):
    data = Note.query.all()
    edit = Note.query.get(id)
    return render_template("notes.html", data=data, edit=edit, role=session.get("role"))

@app.route("/update_note/<int:id>", methods=["POST"])
def update_note(id):
    n = Note.query.get(id)
    n.subject = request.form["subject"]
    n.link = request.form["link"]
    db.session.commit()
    return redirect("/notes")


with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="ajamhs92@gmail.com").first():
        db.session.add(User(name="Ayush Ashwani Jaiswal", email="ajamhs92@gmail.com", password="Ayush@8271", role="admin"))
        db.session.commit()

app.run(debug=True)
