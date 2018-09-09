FROM mvertes/alpine-mongo:4.0.1-0

COPY ./scripts /docker-entrypoint-initdb.d
COPY ./health-check.sh /usr/src/app/health-check.sh

HEALTHCHECK CMD [ "sh", "/usr/src/app/health-check.sh" ]