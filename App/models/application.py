from datetime import datetime
from App.database import db
from App.models import applicant


class Application(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    applicantID = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
    jobID = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    recruiterID = db.Column(db.Integer, db.ForeignKey('recruiter.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    application_status = db.Column(db.Boolean, default=None)

    def __init__(self, applicantID, jobID, recruiterID):
        self.applicantID = applicantID
        self.jobID = jobID
        self.recruiterID = recruiterID

    def __repr__(self):
        return f'Application {self.id} Job {self.jobID} By {self.recruiters.name}, Application Made at {self.application_date.strftime("%Y-%m-%d %H:%M")}, Status {self.application_status}'