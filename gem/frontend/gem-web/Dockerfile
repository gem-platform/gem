FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled
COPY ./fullchain.pem /etc/nginx/ssl/fullchain.pem
COPY ./privkey.pem /etc/nginx/ssl/privkey.pem
COPY ./chain.pem /etc/nginx/ssl/chain.pem