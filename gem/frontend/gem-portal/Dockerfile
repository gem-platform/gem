FROM node:10-alpine

# install all the dependences
WORKDIR /usr/src/lib
COPY package.json .
RUN npm install nuxt -g
RUN npm install
RUN mkdir -p /usr/src/app && mv /usr/src/lib/node_modules /usr/src/app/

# copy sources
WORKDIR /usr/src/app
COPY . /usr/src/app

ENV HOST 0.0.0.0
EXPOSE 3000

RUN npm run build

CMD [ "npm", "run", "start" ]
