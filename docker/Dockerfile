FROM python:3.6

ARG PIP_EXTRA_INDEX_URL

COPY . /usr/src/app/
WORKDIR /usr/src/app/

RUN ./docker/docker-entrypoint.sh echo 'dependencies installed'

ENTRYPOINT ["./docker/docker-entrypoint.sh"]
