FROM node:9

WORKDIR /usr/src/app

COPY . .
RUN npm install

ENV HOST 0.0.0.0
EXPOSE 3000

CMD [ "npm", "run", "dev" ]
