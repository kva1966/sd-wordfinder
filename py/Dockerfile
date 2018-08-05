FROM python:3.7.0-alpine3.8
MAINTAINER Kamal Advani "kamal.advani@namingcrisis.net"

# Env
ENV REFRESHED_AT 2018-08-05-1047
ENV PYTHONPATH PYTHONPATH=wordfinder:${PYTHONPATH}
ENV SD_WORDFINDER_CONTAINER true

# Data
ADD wordfinder /app/wordfinder
COPY requirements.txt /app

# Container Installs
RUN pip install -r /app/requirements.txt

WORKDIR /app
CMD ["python", "-m", "wordfinder.web.app"]
#CMD ["ls", "-alh"]
