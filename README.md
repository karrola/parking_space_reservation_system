# Red-Black Tree – Parking Space Reservation System

This project was created as part of the recruitment task for the web section of the BIT Student Research Group at AGH.

## Technologies

Python, Django, SQLite, HTML5 + Django Templates, Bootstrap 5

## Features

- Booking parking spaces
- Viewing a user’s reservations
- Editing and canceling existing reservations
- admin panel supported by django-admin

## Setup Instructions

1. Clone the repository
2. (Recommended) Create a virtual environment
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Apply database migrations:
```
py manage.py migrate # Windows
python3 manage.py migrate # Linux / macOS
```
5. To use the Django admin panel, create a superuser:
```
py manage.py createsuperuser # Windows
python3 manage.py createsuperuser # Linux / macOS
```
6. Run the development server:
```
py manage.py runserver # Windows
python3 manage.py runserver # Linux / macOS
```

The application will be available at: http://127.0.0.1:8000/  
The admin panel is available at: http://127.0.0.1:8000/admin/  

After logging in as a superuser, you can easily add sample parking spaces in the admin panel to test the application.

## Security Notes

This project was created for recruitment purposes – the `SECRET_KEY` is public and intended only for local development.  
In a production environment, the key should be stored in environment variables.

## AI Usage

AI (ChatGPT) was used as support for debugging code, writing tests, and creating interface elements (Bootstrap classes).
