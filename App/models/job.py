from App.database import db
from App.models import recruiter
from App.models.application import Application
from App.models.recruiter import *

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiterID = db.Column(db.Integer, db.ForeignKey('recruiter.id'), nullable=False)
    job_type = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.String(32), nullable=False)
    applicants = db.relationship('Applicant', secondary='application', backref='applications')
    
    def __init__(self, recruiterID, job_type, salary):
        self.recruiterID = recruiterID
        self.job_type = job_type
        self.salary = salary

    def __repr__(self):
        return f'Job {self.id}: Added By {self.recruiters.name}, {self.job_type}, {self.salary}'
