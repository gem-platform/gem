FROM nginx:1.15-alpine

ARG env

# copy config depends on environment
COPY ./sites-enabled/gem-web-client.${env}.conf /etc/nginx/conf.d/default.conf

# site should be accesible
HEALTHCHECK  --interval=5m --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1