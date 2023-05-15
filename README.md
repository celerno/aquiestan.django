![Python application](https://github.com/django-cms/django-cms-quickstart/workflows/Python%20application/badge.svg?branch=main)

# Aquí están | Dockerseid Django CMS quickstart

"Aquí están" es un proyecto completamente dockerizado listo para ejecutarse en cualquier ambiente que soporte docker. El paquete viene preconfigurado con python 3.9 y django 3.2 con django cms 3.11.

## Installation

El único prerequisito es tener instalado docker: 
- [Instalar Docker](https://docs.docker.com/engine/install/).
- Si nunca has usado docker antes [Introducción a docker](https://docs.docker.com/get-started/).

## Pasos para instalar y ejecutar por primera vez

```bash
git clone git@github.com:django-cms/django-cms-quickstart.git
cd django-cms-quickstart
docker compose build web
docker compose up -d database_default
docker compose run web python manage.py migrate
docker compose run web python manage.py createsuperuser
docker compose up -d
```

Después ejecutar http://django-cms-quickstart.127.0.0.1.nip.io:8000 (o solo http://127.0.0.1:8000) en tu browser.

## Sobre el projecto

Los únicos datos precargados del paquete son el menú. Para proceder a configurar el contenido de la página de inicio y las entradas de blog proceder a /admin e introducir los datos de superuser creados en el paso anterior. 

#### Updating requirements

Para actualizaciones leer detenidamente: https://blog.typodrive.com/2020/02/04/always-freeze-requirements-with-pip-compile-to-avoid-unpleasant-surprises/


#### Env variables
- to deploy this project in testing mode (recommended) set the environment variable `DEBUG` to `True` in your hosting environment. 
- For production environment (if `DEBUG` is false) django requires you to whitelist the domain. Set the env var `DOMAIN` to the host, i.e. `www.domain.com` or `*.domain.com`.
- If you want the media hosted on S3 set the `DEFAULT_FILE_STORAGE` variable accordingly.

#### Deployment Commands
Configure your hosting environment to run the following commands on every deployment:
- `./manage.py migrate`
