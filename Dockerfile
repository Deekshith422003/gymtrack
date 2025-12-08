FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

CMD exec gunicorn gymtrack.wsgi:application --bind 0.0.0.0:$PORT
