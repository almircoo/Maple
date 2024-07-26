FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /code/maple/
RUN  apt-get update && \
     apt-get install  default-libmysqlclient-dev gettext -y && \
      rm -rf /var/lib/apt/lists/*
ADD requirements.txt requirements.txt
RUN pip install --upgrade pip  && \
        pip install --no-cache-dir -r requirements.txt  && \
        pip install --no-cache-dir gunicorn[gevent] && \
        pip cache purge
        
ADD . .
RUN chmod +x /code/maple/bin/docker_start.sh
ENTRYPOINT ["/code/maple/bin/docker_start.sh"]
