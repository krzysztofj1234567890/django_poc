# DJango

## Installation

To install Django 5.0, you will need Python 3.10 or better

The first step is to create a virtual environment in which you will install Django.

### create a virtual environment

```
sudo apt install python3.11-venv
python3 -m venv django-env

# active virtual env
source django-env/bin/activate

## deactivate virtual env
deactivate
```

### install Django
```
pip install django
```

check version:
```
django-admin --version
```

### Create a new Django project

Django instances are organized into two tiers: 
* A __project__ is an instance of Django with its own database configuration, settings, and apps. It’s best to think of a project as a place to store all the site-level configurations you’ll use.
* An __app__ is a subdivision of a project, with its own route and rendering logic. Multiple apps can be placed in a single Django project.

To create a new Django project from scratch, enter the directory where you want to store the project:
```
django-admin startproject project_1
```

The newly created directory should contain a manage.py file, which is used to control the app’s behavior from the command line, and a subdirectory.

Test the project to ensure it’s functioning:
```
cd project_1
python3 manage.py runserver
```

Check:
```
http://127.0.0.1:8000/
```

### Create Django app

Create an application inside of this project:
```
python3 manage.py startapp kjapp
```

This creates a subdirectory for an app.

To start working with the app, you need to first register it with the project. Edit myproj/__settings.py__ as follows, adding a line to the top of the INSTALLED_APPS list:
```
vi project_1/project_1/settings.py

INSTALLED_APPS = [
    'kjapp.apps.KjappConfig',   <----------------- from project_1/kjapp/apps.py
    'django.contrib.admin',
    'django.contrib.auth',
    ...
```

If you look in project_1/kjapp/apps.py, you’ll see a pre-generated object named MyappConfig, which we’ve referenced here

#### Adding routes and views to your Django app

Django applications follow a basic pattern for processing requests:
* When an incoming request is received, Django parses the URL for a __route__ to apply it to.
* Routes are defined in __urls.py__, with each route linked to a __view__, meaning a function that returns data to be sent back to the client. Views can be located anywhere in a Django project, but they’re best organized into their own __modules__.
* Views can contain the results of a __template__, which is code that formats requested data according to a certain design.


Routes are defined in urls.py in a list named urlpatterns. By default, Django creates an admin path that is used for site administration, but we need to create our own routes.
Add another entry, so that the whole file looks like this:

```
vi project_1/project_1/urls.py

from django.urls import path, include     <-----------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('kjapp/', include('kjapp.urls'))   <---------
]
```

Create a new urls.py in kjapp and add the following:

```
vi project_1/kjapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)
]
```

##### Views 

Django views are Python functions that take http requests and return http response, like HTML documents.

Edit the file kjapp/views.py so it looks like this:
```
vi project_1/kjapp/views.py

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world!")
```

To test restat server:
```
python3 manage.py runserver
```
and check result in:
```
http://127.0.0.1:8000/kjapp/
```

#### Adding routes with variables

Django can accept routes that incorporate variables as part of their syntax. Let’s say you wanted to accept URLs that had the format year/<int:year>. 

```
vi project_1/kjapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('year/<int:year>', views.year)       <---------------------
]
```

Then add this function:
```
vi project_1/kjapp/views.py

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world!")
def year(request, year):
    return HttpResponse('Year: {}'.format(year))
```

restart the server and test it:
```
python3 manage.py runserver
http://127.0.0.1:8000/kjapp/year/2010
```

### Django templates

Django’s built-in template language can be used to generate web pages from data.

Templates used by Django apps are stored in a directory that is central to the project: project_1/kjapp/templates/kjapp/

```
vi project_1/kjapp/templates/kjapp/city.html

City: {{city}}
```

Any value within double curly braces in a template is treated as a variable.

```
vi project_1/kjapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('year/<int:year>', views.year),
    path('age/<int:age>', views.age)
]
```

Then add this function:
```
vi project_1/kjapp/views.py

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world!")
def year(request, year):
    return HttpResponse('Year: {}'.format(year))
def age(request, age):
    data = {'age':age}
    return render(request, 'kjapp/age.html', data)
```

### Models

The models.py file contains a description of the database table, as a Python class. 
This is called a model. 
Using this class, you can create, retrieve, update, and delete records in your database using simple Python code rather than writing repetitive SQL statements.

```
vi project_1/kjapp/models.py

from django.db import models
class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
```

run a command to actually create the table in the database:
```
python3 manage.py makemigrations kjapp 
```

Django creates a file describing the changes and stores the file in the /migrations/ folder.

Run the migrate command to  create and execute an SQL statement, based on the content of the new file in the /migrations/ folder:
```
python3 manage.py migrate 
```

check:
```
python3 manage.py sqlmigrate kjapp 0001
```

Use the Python interpreter (Python shell) to add some members:
```
python3 manage.py shell 

from kjapp.models import Member 
member = Member(firstname='Emil', lastname='Refsnes')
member.save() 
Member.objects.all().values() 
```

Add template:
```
vi project_1/kjapp/templates/kjapp/all_members.html

<!DOCTYPE html>
<html>
<body>
<h1>Members</h1> 
<ul>
  {% for x in mymembers %}
    <li>{{ x.firstname }} {{ x.lastname }}</li>
  {% endfor %}
</ul>
</body>
</html>

```

Update view:
```
vi project_1/kjapp/views.py

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import loader                  <--------
from .models import Member                          <--------
def index(request):
    return HttpResponse("Hello, world!")
def year(request, year):
    return HttpResponse('Year: {}'.format(year))
def age(request, age):
    data = {'age':age}
    return render(request, 'kjapp/age.html', data)
def members(request):                                   <--------
  mymembers = Member.objects.all().values()             
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
```

Update urls:
```
vi project_1/kjapp/urls.py

urlpatterns = [
    path('', views.index),
    path('year/<int:year>', views.year),
    path('age/<int:age>', views.age),
    path('members', views.members)                     <--------
]
```

restart the server and test it:
```
python3 manage.py runserver
http://127.0.0.1:8000/kjapp/members
```

## The Definitive Guide to Django: Web Development Done Right by Adrian Holovaty, Jacob K. Moss

