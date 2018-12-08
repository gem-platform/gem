FROM gem-server:latest

RUN apt-get update && apt-get install -y \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
RUN pip3 install weasyprint gunicorn flask

ADD ./fonts/* /root/.fonts/
WORKDIR /usr/src/app
COPY . .

CMD gunicorn --bind 0.0.0.0:4999 main:APP
