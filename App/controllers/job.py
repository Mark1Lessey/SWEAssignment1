from sqlite3 import IntegrityError
from App.database import db
from App.models.application import Application
from App.models.job import Job

def create_job(recruiterID, jobtype, salary):
    try:
        job = Job(recruiterID, jobtype, salary)
        db.session.add(job)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True

def list_jobs():
    allJobs = Job.query.all()
    if allJobs != None:
        for a in allJobs:
            print(a)

def list_job_applicants(jobID):
    applicantsL = Job.query.filter_by(id=jobID).first()
    if applicantsL != None:
        print( f'Applicants for {applicantsL.job_type} Position by {applicantsL.recruiters.name}: \n')

    applicantList = Job.query.filter_by(id=jobID)    
    if applicantList != None:
        for a in applicantList:
            print(f'Application {a.id}: {a.applicants}')