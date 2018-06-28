FROM alpine:3.6

RUN apk add --no-cache sphinx python3
RUN pip3 install --no-cache-dir pymongo

EXPOSE 9306 9312
VOLUME /var/lib/sphinx /etc/sphinx

COPY docker-entrypoint.sh /
COPY sphinx.conf /etc/sphinx/sphinx.conf
COPY index_laws.py /
RUN mkdir -p /var/lib/sphinx/data && mkdir -p /var/log/sphinx/ && mkdir -p /var/run/sphinx 
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["searchd", "--nodetach"]
