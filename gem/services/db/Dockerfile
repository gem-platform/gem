FROM mongo:latest

# copy scripts
COPY ./scripts /docker-entrypoint-initdb.d
COPY ./health-check.sh /usr/src/app/health-check.sh
