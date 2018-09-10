FROM nginx:1.15-alpine

ARG env

COPY ./sites-enabled/gem-web-client.${env}.conf /etc/nginx/conf.d/default.conf
