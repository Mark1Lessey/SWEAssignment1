from sqlite3 import IntegrityError
from App.database import db
from App.models.recruiter import Recruiter

def create_recruiter(name):
    try:     
        recruiter = Recruiter(name)
        db.session.add(recruiter)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True

def list_recruiters():
    allRecruiters = Recruiter.query.all()
    if allRecruiters != None:
        for a in allRecruiters:
            print(a)