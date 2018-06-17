FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled
COPY ./gem.crt /etc/nginx/ssl/gem.crt
COPY ./gem.key /etc/nginx/ssl/gem.key
