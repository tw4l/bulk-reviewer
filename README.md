# Bulk Redactor

This repository is a work in progress.

## Development installation

(requires Docker CE and Docker-Compose)

### Start containers

```
docker-compose up -d
```

The first time you do this, it will take a while. Much of this time is set in installing dependencies for and then building bulk_extractor.

### Create a superuser

```
docker-compose exec server python3 manage.py createsuperuser
```

Follow the instructions to create a user with full admin rights.

### Django admin interface

Visit [localhost:8000/admin](http://localhost:8000/admin) in browser.

### Tox

To run Tox/flake8 locally, create a `/usr/share/bulk_extractor` (Linux) or `/usr/local/share/bulk_extractor` (macOS) directory and move the helper scripts in the `server/bulk_extractor` directory into it. This will place required Python DFXML libraries into their expected paths; otherwise you may encounter module import errors.