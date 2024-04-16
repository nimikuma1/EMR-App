from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))

class Emr(db.Model):
    memberID = db.Column(db.Integer, primary_key=True)
    memberName = db.Column(db.String(255))  # New column 'memberName'
    memberSex = db.Column(db.String(1))
    memberDOB = db.Column(db.Date)
    payor = db.Column(db.String(100))
    clinicalNotes = db.Column(db.Text)
    ICDCode = db.Column(db.Text)
    procedureCode = db.Column(db.String(100))
    priorAuthStatus  = db.Column(db.String(10))




   


