FROM gem-server:latest


WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# site should be accesible
HEALTHCHECK  --interval=1m \
  CMD wget --quiet --tries=1 --spider http://localhost:5000/api/health || exit 1

CMD [ "python", "-u", "/usr/src/gem-server-common/_runner.py" ]