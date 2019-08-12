# Core
Django project structure

---
### Install Python dependencies
```sh
$ pip install -r requirements/develop.txt
```

---
### Setup project folder structure
```sh
$ mkdir logs
$ mkdir fixtures
$ mkdir public/compress
```

---
### Setup Project initial data
`createsuperadmin` script will create a superadmin with:
* username: admin
* password: Snapdec2018!
```sh
$ ./manage.py migrate
$ ./manage.py createsuperadmin -f
```
