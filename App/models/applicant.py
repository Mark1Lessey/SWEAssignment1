from App.database import db

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    contact = db.Column(db.String(128), nullable=False)

    def __init__(self, fullname, email, contact):
        self.fullname = fullname
        self.email = email
        self.contact = contact


    def __repr__(self):
        return f'Applicant {self.id} {self.fullname}, {self.email}, {self.contact}' 

