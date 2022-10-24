FROM node:18.11.0-bullseye-slim

RUN mkdir /app/ /app/src/ /.npm/
WORKDIR /app
ADD *.json *.js *.yaml *.yml /app/
COPY public/ /app/public
RUN chown -R node:node /app/ /.npm/ \
 && chmod -R 777 /app/ /.npm/
USER node
RUN npm install

ENTRYPOINT [ "npm" ]
