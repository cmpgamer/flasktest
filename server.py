from flask import Flask, render_template, redirect, request, session
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from db import Base, init_db, m_testengine
import db
from models import StudentModel

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
 
@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html')

@app.route("/session")
def testsession():
    return render_template('index.html')

@app.route("/db")
def initialize():
    init_db('sqlite:///tmp/test.db')
    init_db('sqlite:///tmp/test1.db')

    return redirect('/')

 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")
 
 
@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/test")
def test():
    db.m_testengine = create_engine('sqlite:///tmp/test.db', convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db.m_testengine))
    from models import StudentModel
    db_session.add(StudentModel('Bryan', 'bmnosar@gmail.com'))
    db_session.commit()
    return redirect("/")

@app.route("/test1")
def test1():
    db.m_testengine = create_engine('sqlite:///tmp/test1.db', convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db.m_testengine))
    from models import StudentModel
    db_session.add(StudentModel('James', 'jimmy@yahoo.com'))
    db_session.commit()
    return redirect("/")

@app.route("/query")
def querydb():
    # db_session = scoped_session(sessionmaker(autocommit=False,
    #                                      autoflush=False,
    #                                      bind=m_testengine))
    from models import StudentModel
    db_session = sessionmaker(db.m_testengine)
    with db_session() as ses:
        print(ses.query(StudentModel).all())

    return redirect("/")
 
if __name__ == "__main__":
    app.run(debug=True)