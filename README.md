# UserAuth
A project that applies most of the user authentication and authorization functionalities.

To Run The project You Need To

- Create a virtual environment:

  $ virtualenv venv

- Activate the environment:

  $ source venv/bin/activate
  
- Install the requirements:

  $ pip install -r requirements.txt
  
- Migrate the database

  $ python manage.py makemigrations users
  
- Apply migrations to the database

  $ python manage.py migrate
  
- You can run tests of the project before starting the server
  
  $ python manage.py test
  
- After that start the server and run the project

  $ python manage.py runserver
  
  
