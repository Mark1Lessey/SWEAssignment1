from App.database import db

class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    jobs = db.relationship('Job', backref='recruiters')
    applications = db.relationship('Application', backref='recruiters')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Recruiter {self.id}: {self.name}'
