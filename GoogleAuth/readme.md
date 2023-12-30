Certainly! Below is the formatted content for your README.md file:

# Google Authentication and Fetching Emails with Django

This guide will walk you through setting up Google authentication and extracting emails using Django 2.0, Google API Python client, and oauth2client. We will use Google API Python client for interacting with the API and oauth2client for handling authentication. 

## Step 1: Creating Django Project

Start by creating a virtual environment and installing Django:

```bash
mkdir google-login && cd google-login
python3.5 -m venv myvenv
source myvenv/bin/activate
pip install Django==2.0.7
django-admin startproject gfglogin .
django-admin startapp gfgauth
```

Add 'gfgauth' to the `INSTALLED_APPS` list in `settings.py`. Then, migrate the project:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Step 2: Installing Dependencies

Install required modules: google-api-python-client, oauth2client, and jsonpickle:

```bash
pip install google-api-python-client==1.6.4
pip install oauth2client==4.1.2
pip install jsonpickle==0.9.6
```

## Step 3: Creating Models

Define models in `models.py` for storing credentials:

```python
# gfgauth/models.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    credential = CredentialsField()
    task = models.CharField(max_length=80, null=True)
    updated_time = models.CharField(max_length=80, null=True)

class CredentialsAdmin(admin.ModelAdmin):
    pass
```

Modify the import in `__init__.py` to fix Django 2.0 compatibility:

```python
# myvenv/lib/python3.5/site-packages/oauth2client/contrib/django_util/__init__.py

from django.urls import reverse
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 4: Creating Views

Define views in `views.py` for Google authentication:

```python
# gfgauth/views.py

from django.shortcuts import render, HttpResponseRedirect
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.client import flow_from_clientsecrets
from django.http import HttpResponseBadRequest
import httplib2
from apiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from oauth2client import xsrfutil
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.db import models

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/gmail.readonly',
    redirect_uri='http://127.0.0.1:8000/oauth2callback',
    prompt='consent'
)

@login_required
def gmail_authenticate(request):
    # ... (as per your existing code)

@login_required
def auth_return(request):
    # ... (as per your existing code)

@login_required
def home(request):
    # ... (as per your existing code)
```

## Step 5: Creating URLs and Basic Settings

Configure URLs in `urls.py`:

```python
# gfglogin/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gfgauth.urls')),
]
```

Configure app-specific URLs in `gfgauth/urls.py`:

```python
# gfgauth/urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gmailAuthenticate', views.gmail_authenticate, name='gmail_authenticate'),
    url(r'^oauth2callback', views.auth_return),
    url(r'^$', views.home, name='home'),
]
```

Update `settings.py`:

```python
# settings.py

# ... (existing settings)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        # ...
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = 'client_secrets.json'
```

## Step 6: Generating OAuth2 Client Secret File

1. Head over to [Google Developer Console](https://console.developers.google.com/).
2. Create a new project and name it.
3. Navigate to API services > Credentials.
4. Click on create credentials and select "Web application."
5. Set a name, specify the redirect URI as `http://127.0.0.1:8000/oauth2callback`, and save.
6. Download the credentials file (it will be in JSON format).
7. Rename the downloaded file to `client_secrets.json` and place it in the project root.

## Step 7: Running the Application

Ensure everything is set up correctly:

```bash
python3.5 manage.py makemigrations
python3.5 manage.py migrate
```

Create a superuser:

```bash
python3.5 manage.py createsuperuser
```

Run the server:

```bash
python3.5 manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser, log in with the superuser credentials, and click on the Google link to test the authentication flow.

For the full code, refer to the [repository](#) (replace with your repository link).