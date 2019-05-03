# Django Rest Framework Firebase Authentication

This package provides a base Firebase Authentication backend class for the Django rest framework. Two key methods are not implemented for more flexebility. Let's [keep it simple, stupid](https://en.wikipedia.org/wiki/KISS_principle).

## Requirements

- Python 2.7 or 3.4+
- [Django](https://github.com/django/django) (version 1.11+)
- [Django Rest Framework](https://github.com/encode/django-rest-framework)
- [Firebase Admin Python](https://github.com/firebase/firebase-admin-python)

## Installation

```pip install drf-firebase-authentication```

## Usage

#### 1. Subclass `BaseFirebaseAuthentication` and implement its template methods:

Decide by yourself how you want to associate Firebase users with local django users by implementing the `.get_django_user()` method accordingly.

Put your code into a `authentication.py` file inside an app dedicated to your projects REST Api.

```python
from drf_firebase.authentication import BaseFirebaseAuthentication
from firebase_admin import credentials, initialize_app
from django.contrib.auth import get_user_model

firebase_creds = credentials.Certificate('path/to/firebase/credentials.json')
firebase_app = initialize_app(firebase_creds)

class FirebaseAuthentication(BaseFirebaseAuthentication):
	"""
	Example implementation of a DRF Firebase Authentication backend class
	"""
	def get_firebase_app(self):
		return firebase_app

	def get_django_user(self, firebase_user_record):
		return get_user_model().objects.get_or_create(
			username=firebase_user_record.uid,
		)[0]
```

#### 2. Add the just created Firebase authentication backend to your `settings.py`:

Replace `YOUR_RESTAPI_APP` with the app you put your `authentication.py` file in.

```python
REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.SessionAuthentication', # default
		'rest_framework.authentication.BasicAuthentication', # default
		'YOUR_RESTAPI_APP.authentication.FirebaseAuthentication',
	),
}
```