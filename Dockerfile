FROM python:3.11-slim

RUN apt-get update && apt-get install -y supervisor

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-cache-dir

ADD . /app
WORKDIR /app

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PYTHONPATH=/app

CMD ["/usr/bin/supervisord"]
