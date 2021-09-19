FROM python:3.7

RUN mkdir /code

WORKDIR /code

COPY . /code/

RUN pip install -r /code/requirements.txt

CMD python manage.py runserver 0.0.0.0:8000