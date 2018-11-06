# Djoser-Angular
Django backend authentication using Djoser with Angular frontend

1. Create virtualenv using [pipenv](https://pipenv.readthedocs.io/en/latest/)
	```
	pipenv install django djangorestframework djangorestframework-jwt djoser python-decouple
	# activate virtualenv using
	pipenv shell
	```

2. Start django project
	```
	# ending dot creates files in the same folder
	django-admin startproject backend .
	ng new frontend
	```

	**Don't run django migrate command for now.**

3. Start django app for custom user model
	```
	python manage.py startapp users
	```

	**You can find the code for the custom user model from the same repo folder 'users'.**

4. Specify the custom user model in django **settings** by

	```
	# backend/settings.py
	INSTALLED_APPS = [
		'users',
	]
	# specify user model
	AUTH_USER_MODEL = 'users.User'
	```

	**Now run the makemigrations and migrate command**

4. Start angular project using [Angular CLI](https://cli.angular.io/)
	```
	// styling files will be in 'scss' format and routing file will be pre initiated.
	ng new frontend --style=scss --routing
	```

5. Try out the project progress so far by running django and angular server

	```
	python manage.py runserver
	```

	In another command prompt run angular server
	```
	cd frontend
	ng serve -o
	```

### Project is under construction.
