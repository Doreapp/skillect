FROM node:18.11.0-bullseye-slim

RUN mkdir /app/ /app/src/ \
 && chown -R node /app/
WORKDIR /app

ADD *.json *.js /app/
COPY public/ /app/public
RUN npm install

ENTRYPOINT [ "npm" ]
