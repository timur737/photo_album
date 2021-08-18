# Photo Album

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/timur737/photo_album.git
$ cd photo_album
```
And you need create virtualenv
```sh
$ python3.9 -m venv venv
$ . venv/bin/activate
```
After that
```sh
$ pip install -r requirements.txt
$ python manage.py makemigrations && python manage.py migrate
$ python manage.py runserver
```
### You can see APIs on two documentation Redoc and Swagger
Swagger http://0.0.0.0:8000/api/v1/swagger/
Redoc http://0.0.0.0:8000/api/v1/redoc/

NOTES:
First of all you register on /register/ endpoint which you need to send to the body username and password.
after that you need get Token from /login again paste in body your username and password

and your API requests should have an Authentication header.

