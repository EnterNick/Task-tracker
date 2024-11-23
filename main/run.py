import os


if __name__ == '__main__':
    os.system('daphne -b 0.0.0.0 -p 8001 main.asgi:application')
    os.system('python manage.py runserver 0.0.0.0:8000')
