# Glik's backend composer

> The backend composer application of Glik.

## Requirements

- [Docker](https://www.docker.com/) (needed)
- [Docker Compose](https://docs.docker.com/compose/) (needed)
- [Make](https://en.wikipedia.org/wiki/Make_(software)) (highly recommended)
- [Poetry](https://python-poetry.org/docs/) (highly recommended)

## Install for local development

Create your local settings at each submodule (_i.e._, environment variables)

```bash
make setlocalenv
```

Build the images

```bash
docker-compose build --parallel
```

Optional: drop the database

```bash
docker-compose down --volumes
```

Run the migrations

(Tip: the database might not be ready yet; if it fails then try again)

```bash
make migrate
```

Run the application

```bash
docker-compose up
```

Stop the apps (on another terminal)

```bash
docker-compose down
```

## Write some code

Create a development-friendly virtual environment (do the same at each submodule)

```bash
make createvenv
```

Un-ignore new files at the `.dockerignore` of each submodule as needed.
