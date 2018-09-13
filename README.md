![Bulk Reviewer logo](https://github.com/timothyryanwalsh/bulk-reviewer/blob/master/docs/assets/img/full-logo.png)

## About

### Identify, review, and remove sensitive files.

Bulk Reviewer is intended to help librarians, archivists, and others to identify, review, and remove sensitive files in directories and disk images, built in [Django](https://www.djangoproject.com/), [Django Rest Framework](http://www.django-rest-framework.org/), [Django Channels](https://channels.readthedocs.io/en/latest/), and [Vue.js](https://vuejs.org/). It scans directories and disk images for personally identifying information (PII) and other sensitive information using [bulk_extractor](https://github.com/simsong/bulk_extractor), a best-in-class digital forensics tool, and presents results in a review dashboard, enabling easier detection and dismissal of false positives. Bulk Reviewer provides the ability to generate CSV reports about inputs as well as the ability to export files from directories and disk images, separating problematic files from those that are free of sensitive information.

Initial development occurred while the author, Tim Walsh, was a 2018 Summer Fellow at the [Library Innovation Lab](https://lil.law.harvard.edu) at Harvard University. The application is currently under active development, and is still in the exploratory/prototype phase.

Interested in getting involved? [Get in touch](mailto:timothyryanwalsh@gmail.com)!

## Development installation

Requires [Docker CE](https://www.docker.com/community-edition) and [Docker-Compose](https://docs.docker.com/compose/). A powerful machine with plenty of cores and RAM to spare is recommended, as bulk_extractor, Daphne (Django ASGI server), and the Webpack dev server collectively use a lot of resources.

### Clone repository to local machine

```
git clone https://github.com/timothyryanwalsh/bulk-reviewer.git
cd bulk-reviewer
```

### Configure docker-compose volumes

The current configuration for sharing data between the host development machine and the `server` and `worker` Docker containers assumes a macOS development environment. Development in Linux or Windows may require changing the volume configuration to be appropriate for the local machine:

```
- /Users:/Users
- /Volumes:/Volumes
```

These two volumes are used only for giving the `worker` and `server` containers access to data to scan with bulk_extractor. For development on Linux or Windows, change these two volumes for the `worker` and `server` containers in `docker-compose.yml` to appropriate values such as `- /home:/home` (Linux) or `- C:\Users:/Users` (Windows) - this will determine which directories/files are accessible to Bulk Reviewer from the host machine.

### Start containers

```
docker-compose up -d
```

The first time you do this, it will take a while (on my laptop, around 10 minutes). Much of this time is spent installing dependencies for and then building bulk_extractor.

### Start frontend development server

```
cd client
```
Install node_modules (required first time only):

```
npm install
```

Start webpack dev server:

```
npm run dev
```

### Open application in browser

Open [127.0.0.1:8080](http://127.0.0.1:8080) in your browser.

### Tox

To run Tox/flake8 locally, create a `/usr/share/bulk_extractor` (Linux) or `/usr/local/share/bulk_extractor` (macOS) directory and move the helper scripts in the `server/bulk_extractor` directory into it. This will place required Python DFXML libraries into their expected paths; otherwise you may encounter module import errors.
