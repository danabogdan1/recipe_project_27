This is our django web server, for recipe management.

To get started, run:

python -m venv .venv
make sure you activate the virtual environment after running the previous command.
Then run:
pip install -r requirements.txt

This will setup your virtual env, and install the required packages.

Web Pages (URLs)

- `/` — Home page (list all recipes)
- `/recipes/alphabetical/` — List recipes alphabetically
- `/recipes/by_date/` — List recipes by date
- `/recipe/<id>/` — View recipe details
- `/recipe/add/` — Add a new recipe
- `/recipe/<id>/edit/` — Edit a recipe
- `/recipe/<id>/delete/` — Delete a recipe
- `/register/` — Register a new user
- `/login/` — User login page
- `/logout/` — User logout 

To run tests:

pytest

To start the webserver, run:

python manage.py runserver