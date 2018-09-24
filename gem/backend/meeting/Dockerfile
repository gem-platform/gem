FROM gem-server:latest


WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8090
EXPOSE 8099

# site should be accesible
HEALTHCHECK  --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:8099 || exit 1

CMD [ "python", "-u", "/usr/src/gem-server-common/_runner.py" ]