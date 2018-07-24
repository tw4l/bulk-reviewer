# Bulk Redactor

**Work in progress.**

![Bulk Redactor logo](https://github.com/timothyryanwalsh/bulk-redactor/blob/master/full-logo.jpg)

## Development installation

(requires Docker CE and Docker-Compose)

### Run init_default.sh script

```
chmod u+x init_default.sh
./init_default.sh
```

This script creates a `data` directory which is mounted in the Docker containers as a volume. The `data` directory is intended for user data, and contains three sub-folders:

* `data/transfers/`: A location for users to place disk images and directories to scan.
* `data/logs/`: Where Bulk Redactor writes redaction logs.
* `data/redacted/`: Where Bulk Redactor writes redacted files and disk images.

### Start containers

```
docker-compose up -d
```

The first time you do this, it will take a while (on my laptop, around 10 minutes). Much of this time is spent installing dependencies for and then building bulk_extractor.

### Frontend

Start webpack dev server:

```
cd client
npm install
npm run dev
```

Visit [localhost:8080](http://localhost:8080) in your browser

### Tox

To run Tox/flake8 locally, create a `/usr/share/bulk_extractor` (Linux) or `/usr/local/share/bulk_extractor` (macOS) directory and move the helper scripts in the `server/bulk_extractor` directory into it. This will place required Python DFXML libraries into their expected paths; otherwise you may encounter module import errors.