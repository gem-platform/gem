FROM nginx:1.15-alpine

ARG env

# copy config depends on environment
COPY ./envs/${env}.conf /etc/nginx/conf.d/default.conf
COPY ./configs /etc/nginx

# copy custom error pages
COPY ./maintenance /usr/share/nginx/html
