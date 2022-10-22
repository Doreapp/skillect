FROM node:18.11.0-bullseye-slim

RUN mkdir /app/ /app/src/
WORKDIR /app
ADD *.json *.js /app/
COPY public/ /app/public
RUN chown -R node:node /app/
USER node
RUN npm install

ENTRYPOINT [ "npm" ]
