from sqlite3 import IntegrityError
from App.database import db
from App.models.applicant import Applicant
from App.models.application import Application

def create_applicant(fullname, email, contact):
    try:     
        applicant = Applicant(fullname, email, contact)
        db.session.add(applicant)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True

def list_applicants():
    allApplicants = Applicant.query.all()
    if allApplicants != None:
        for a in allApplicants:
            print(a)


