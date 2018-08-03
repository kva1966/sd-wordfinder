FROM python:3.7.0-alpine3.8
MAINTAINER Kamal Advani "kamal.advani@namingcrisis.net"

# Data
ADD wordfinder /app/wordfinder
COPY requirements.txt /app

# Env
ENV PYTHONPATH PYTHONPATH=wordfinder:${PYTHONPATH}
ENV SD_WORDFINDER_CONTAINER true

# Container Installs
RUN pip install -r /app/requirements.txt

WORKDIR /app
CMD ["python", "-m", "wordfinder.web.app"]
#CMD ["ls", "-alh"]
