# Bulk Reviewer

**Work in progress.**

![Bulk Reviewer logo](https://github.com/timothyryanwalsh/bulk-reviewer/blob/master/docs/assets/img/full-logo.png)

## Development installation

Requires [Docker CE](https://www.docker.com/community-edition) and [Docker-Compose](https://docs.docker.com/compose/).

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

These two volumes are used only for giving the `worker` and `server` containers access to data to scan with bulk_extractor. For development on Linux or Windows, change these two volumes for the `worker` and `server` containers in `docker-compose.yml` to appropriate values such as `- /home:/home` (Linux) or `- C:\Users:/Users` (Windows).

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

Open [127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Tox

To run Tox/flake8 locally, create a `/usr/share/bulk_extractor` (Linux) or `/usr/local/share/bulk_extractor` (macOS) directory and move the helper scripts in the `server/bulk_extractor` directory into it. This will place required Python DFXML libraries into their expected paths; otherwise you may encounter module import errors.
