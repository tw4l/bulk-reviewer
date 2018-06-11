# Bulk Redactor

This respository is a work in progress.

## Development installation

(requires Docker CE and Docker-Compose)

### Start containers

```
docker-compose up -d
```

### Create a superuser

```
docker-compose exec server ./manage.py createsuperuser
```

Follow the instructions to create a user with full admin rights.

### Admin interface

Visit [localhost:8000/admin](http://localhost:8000/admin) in browser.