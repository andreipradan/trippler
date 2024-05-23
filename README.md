# trippler

### Getting started
- prerequisites:
  - poetry installed: https://python-poetry.org/docs/#installation
- run `poetry install`
  - this installs all the dependencies
- `EXPORT DEBUG=True`
    - this sets the django debug env var to tru so it can collect the static files (js, css, img files) and serve them locally
- `poetry run python manage.py createsuperuser`
  - and follow the steps to create an initial super user to access the admin panel and the functionalities without having to manually go through registration
- `poetry run python manage.py ruserver`
  - this starts the django development server and it can be accessed at `http://localhost:8000/`
