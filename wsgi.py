from App.controllers.application import create_application
import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Applicant, Application, Recruiter, Job
from App.main import create_app
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

#@app.cli.command("create_job", help="Allows the recruiter to create jobs for listing")
#@click.argument('')

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Applicant Commands
'''
applicant_cli = AppGroup('applicant', help='Applicant model commands')

@applicant_cli.command('create_applicant', help='Creates an applicant object')
@click.argument('fullname')
@click.argument('email')
@click.argument('contact')
def create_applicant_comand(fullname, email, contact):
    if create_applicant(fullname, email, contact):
        print(f'Applicant "{fullname}" was added.')

@applicant_cli.command("list_applicants", help="Lists applicants registered")
def list_applicant():
    list_applicants()



app.cli.add_command(applicant_cli)

'''
Recruiter Commands
'''
recruiter_cli = AppGroup('recruiter', help='Recruiter model commands')

@recruiter_cli.command('create_recruiter', help='Creates a recruiter object')
@click.argument('name')
def create_recruiter_command(name):
    if create_recruiter(name):
        print(f'Recruiter "{name}" was added.')

@recruiter_cli.command('list_recruiters', help="Lists recruiters registered")
def list_recruiter_comand():
    list_recruiters()

app.cli.add_command(recruiter_cli)

'''
Job Commands
'''

job_cli = AppGroup('job', help='Job model commands')

@job_cli.command('create_job', help='Creates a job object')
@click.argument('recruiternum')
@click.argument('jobtype')
@click.argument('salary')
def create_job_command(recruiternum, jobtype, salary):
    if create_job(recruiternum, jobtype, salary):
        print(f'Job "{jobtype}" was created.')

@job_cli.command('list_jobs', help="Lists jobs registered")
def list_job():
    list_jobs()

@job_cli.command('list_job_applicants', help='List applications that are linked to this Job')
@click.argument('jobnum')
def list_job_applicants_command(jobnum):
    list_job_applicants(jobnum)


app.cli.add_command(job_cli)


'''
Application Commands
'''
application_cli = AppGroup('application', help='Application model commands')

@application_cli.command('create_application', help='create application object')
@click.argument('applicantnum')
@click.argument('jobnum')
@click.argument('recruiternum')
def create_application_command(applicantnum, jobnum, recruiternum):
    if create_application(applicantnum, jobnum, recruiternum):
        applicant = Applicant.query.filter_by(id=applicantnum).first()
        print(f'Application made for', applicant.fullname)
    else:
        print("Application Already Exists")

@application_cli.command('list_applications', help="Lists applications")
def list_application_command():
    list_applications()

app.cli.add_command(application_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)