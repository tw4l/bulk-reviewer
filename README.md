# Bulk Reviewer

**Work in progress.**

![Bulk Reviewer logo](https://github.com/timothyryanwalsh/bulk-redactor/blob/master/full-logo.jpg)

## Development installation

(requires Docker CE and Docker-Compose)

### Clone repository to local machine

```
git clone https://github.com/timothyryanwalsh/bulk-reviewer.git
cd bulk-reviewer
```

### Start containers

```
docker-compose up -d
```

The first time you do this, it will take a while (on my laptop, around 10 minutes). Much of this time is spent installing dependencies for and then building bulk_extractor.

### Frontend

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

Open [127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Tox

To run Tox/flake8 locally, create a `/usr/share/bulk_extractor` (Linux) or `/usr/local/share/bulk_extractor` (macOS) directory and move the helper scripts in the `server/bulk_extractor` directory into it. This will place required Python DFXML libraries into their expected paths; otherwise you may encounter module import errors.