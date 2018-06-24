FROM tutum/nginx

ARG env

RUN rm /etc/nginx/sites-enabled/default
COPY ./sites-enabled/gem-web-client.${env}.conf /etc/nginx/sites-enabled
COPY ./keys /etc/nginx/ssl

#COPY ./fullchain.pem /etc/nginx/ssl/fullchain.pem
#COPY ./privkey.pem /etc/nginx/ssl/privkey.pem
#COPY ./chain.pem /etc/nginx/ssl/chain.pem