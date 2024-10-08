[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli


#COMMANDS FOR ASSIGNMENT 1
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


```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```


# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
