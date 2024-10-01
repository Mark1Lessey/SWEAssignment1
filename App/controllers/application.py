from sqlite3 import IntegrityError
from App.database import db
from App.models import Application

def create_application(applicantsID, jobsID, recruitersID):
    if Application.query.filter_by(applicantID=applicantsID, jobID=jobsID, recruiterID=recruitersID).first() != None:
        return False
    
    try:
        application = Application(applicantsID, jobsID, recruitersID)
        db.session.add(application)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False


def list_applications():
    allApplications = Application.query.all()
    if allApplications != None:
        for a in allApplications:
            print(a)

        


    