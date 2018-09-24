FROM mongo:latest

# copy scripts
COPY ./scripts /docker-entrypoint-initdb.d
COPY ./health-check.sh /usr/src/app/health-check.sh

# db healthcheck
HEALTHCHECK --interval=1m --timeout=30s --start-period=30s --retries=3 \
    CMD [ "sh", "/usr/src/app/health-check.sh" ]