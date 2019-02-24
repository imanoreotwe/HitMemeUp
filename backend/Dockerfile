FROM python:latest


ADD ./default.conf /etc/nginx/conf.d/

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/

ADD . /usr/src/

RUN pip install --no-cache-dir -r requirements.txt

Add ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

CMD uwsgi --ini /etc/uwsgi.ini
