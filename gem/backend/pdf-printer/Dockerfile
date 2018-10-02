FROM alpine:latest

RUN apk --update --upgrade add bash cairo pango gdk-pixbuf py3-cffi py3-pillow py-lxml
RUN pip3 install weasyprint gunicorn flask

ADD ./fonts/* /root/.fonts/
WORKDIR /usr/src/app
COPY . .

CMD gunicorn --bind 0.0.0.0:4999 app:APP

# site should be accesible
HEALTHCHECK  --interval=1m \
  CMD wget --quiet --tries=1 --spider http://localhost:4999/health || exit 1