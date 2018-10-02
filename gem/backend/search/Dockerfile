FROM alpine:3.6

# Install Sphinx and Python
COPY requirements.txt /usr/app/requirements.txt
RUN apk add --no-cache sphinx python3
RUN pip3 install --no-cache-dir -r /usr/app/requirements.txt

# Copy files
COPY sphinx.conf /etc/sphinx/sphinx.conf
COPY . /usr/app
RUN mkdir -p /var/lib/sphinx/data && \
    mkdir -p /var/log/sphinx/ && \
    mkdir -p /var/run/sphinx && \
    chmod +x /usr/app/entrypoint.sh

# Reindex job
COPY reindex /etc/periodic/15min
RUN chmod a+x /etc/periodic/15min/reindex

EXPOSE 9306 9312

HEALTHCHECK --interval=1m --start-period=15s --retries=3 \
    CMD [ "python3", "/usr/app/healtcheck.py" ]

ENTRYPOINT ["/usr/app/entrypoint.sh"]
CMD ["searchd", "--nodetach"]
