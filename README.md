# Survey-Assignment
Clone the project into your local machine 
Make sure you have python installed in your system
Install all the requirements and dependencies using the following command: 
pip install -r requirements.txt 

Default django database SQLite is used. No database setup is needed 
Make Migrations of the models using the following commands: 
python manage.py makemigrations user
python manage.py makemigrations survey
Migrate using the following command: 
python manage.py migrate 

Run the project using the following command: 
python manage.py runserver 
Your project will run at the url : http://127.0.0.1:8000/ (8000 is the default port)

To get a view of the django admin panel (database), create a superuser using the following command. It will ask for your email address, name and password.
python manage.py createsuperuser 
Use the url http://127.0.0.1:8000/admin/ to login in to Django's admin panel. 

