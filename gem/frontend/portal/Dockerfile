FROM node:10-alpine

# install all the dependences
WORKDIR /usr/src/lib
COPY package.json .
RUN npm install && \
    mkdir -p /usr/src/app && \
    mv /usr/src/lib/node_modules /usr/src/app/

# copy sources
WORKDIR /usr/src/app
COPY . /usr/src/app

ENV HOST 0.0.0.0

# site should be accesible
HEALTHCHECK  --interval=5m --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://0.0.0.0:3000/ || exit 1

CMD [ "npm", "run", "start" ]
