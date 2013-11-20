pyKitty
=======

A WebApp written in Django for organizing the communal pool of money for drinks, coffee, snacks, etc. in an office. In Germany it is known as "Kaffeekasse".

Demo
----
http://kitty.pygroup.de/

iPhone Client
-------------

* [KittyClient](https://github.com/CooperRS/KittyClient) (Thanks to Roland Moers)

Requirements
------------

* [Django](https://www.djangoproject.com/download/)
* [django-dajaxice](https://github.com/jorgebastida/django-dajaxice/)
* [django-dajax](https://github.com/jorgebastida/django-dajax/)
* [django-redis](https://github.com/niwibe/django-redis)
* [Node.js](http://nodejs.org/)
* [redis](http://redis.io/)

How to run
----------

To run Django Part
```bash
git clone https://github.com/SimonJakubowski/pyKitty.git
cd pyKitty
python manage.py syncdb
python manage.py runserver
```

To run Node.js Part
```bash
cd nodejs
npm install socket.io
node server.js
```
