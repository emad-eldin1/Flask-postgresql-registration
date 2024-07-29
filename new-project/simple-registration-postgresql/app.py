from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/sampledb'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Your models here
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    email = db.Column(db.String(40))

    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']

    student = Student(fname, lname, email)
    db.session.add(student)
    db.session.commit()

    # Fetch a certain student
    student_result = db.session.query(Student).filter(Student.id == 1).all()
    for result in student_result:
        print(result.fname)

    return render_template('success.html', data=fname)

if __name__ == "__main__":
    app.run(port=7000,debug=True)