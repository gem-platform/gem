FROM alpine:3.6

# Install Sphinx and Python
RUN apk add --no-cache sphinx python3
RUN pip3 install --no-cache-dir pymongo

# Copy files
COPY docker-entrypoint.sh /
COPY sphinx.conf /etc/sphinx/sphinx.conf
COPY *.py /
RUN mkdir -p /var/lib/sphinx/data && mkdir -p /var/log/sphinx/ && mkdir -p /var/run/sphinx 
RUN chmod +x /docker-entrypoint.sh

# Reindex job
COPY reindex /etc/periodic/15min
RUN chmod a+x /etc/periodic/15min/reindex

EXPOSE 9306 9312

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["searchd", "--nodetach"]
