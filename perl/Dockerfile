FROM perl:5.28.0-slim
MAINTAINER Kamal Advani "kamal.advani@namingcrisis.net"

# Env
ENV REFRESHED_AT 2018-09-15-1513
ENV SD_WORDFINDER_CONTAINER true

# Data
ADD lib /app/lib
COPY cpanfile /app

WORKDIR /app

# Dependencies off WORKDIR
# RUN [ "cpanm", "--installdeps", "." ]
RUN [ "cpanm", "--notest", "--installdeps", "." ]

# CMD ["ls", "-alh"]
# CMD perl -e "print qq(@INC)"
# CMD perl -e 'use Mojolicious::Lite;'

CMD ["perl", "-Ilib/", "-mWordFinder::Web::App"]
