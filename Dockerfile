FROM python:3.6.6-alpine

COPY ./requirements /code/requirements

RUN pip install -r /code/requirements/production.pip --no-cache-dir

WORKDIR /code/course_annotation

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "wsgi:application"]