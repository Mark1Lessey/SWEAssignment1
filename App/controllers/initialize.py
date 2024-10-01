from .user import create_user
from .applicant import *
from .job import *
from .recruiter import *
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_applicant('Ethan Joe', 'ethan@email.com', '123-4567')
    create_applicant('Christa Joe', 'christa@email.com', '234-5678')
    create_applicant('Lanaya Joe', 'lanaya@email.com', '345-6789')
    create_applicant('Jada Joe', 'jada@email.com', '456-7890')
    create_recruiter('Google')
    create_recruiter('Apple')
    create_recruiter('Sony')
    create_recruiter('Microsoft')
    create_job('1','Accountant', '$2500')
    create_job('2', 'Doctor', '$3500')
    create_job('3', 'Laywer', '$4500')
    create_job('4', 'Engineer', '$5500')

