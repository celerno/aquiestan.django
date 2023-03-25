FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install aldryn_apphooks_config parler django-taggit django-taggit-autosuggest django-meta django-sortedm2m djangocms-blog
RUN python manage.py collectstatic --noinput
CMD uwsgi --http=0.0.0.0:80 --module=backend.wsgi
