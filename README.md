# django_jwt_auth

## Run locally

To run locally

- Clone this repo:
  ```
   git clone https://github.com/MEsen1/django_jwt_auth.git
  ```
- Change directory into the `backend` folder:
  ```
   cd backend
  ```
- Create a virtual environment:

  ```
   pipenv shell
  ```

  You might opt for other dependencies management tools such as `virtualenv`, `poetry`, or `venv`. It's up to you.

- Install the dependencies:
  ```
  pipenv install
  ```
- Make migrations and migrate the database:
  ```
   python manage.py makemigrations
   python manage.py migrate
  ```
- Finally, run the application:
  ```
   python manage.py runserver
  ```
