# Multi stage dockerfile designated to be used in production

# Stage 0: build and compile frontend
FROM node:18.11.0-bullseye-slim as build-stage

# Generic configuration
RUN mkdir /app/ /.npm/
WORKDIR /app

# Project configuration
ADD *.json *.js *.yaml *.yml /app/
COPY public/ /app/public
COPY src/ /app/src

# Permissions...
RUN chown -R node:node /app/ /.npm/ \
 && chmod -R 777 /app/ /.npm/
USER node

# Build arguments:
#   - URL: protocol and host
# Note: For React to get an env variable, it must be prefixed by `REACT_APP_`
ARG URL=http://localhost
ENV REACT_APP_URL=${URL}

# Install the libraries and build the project
RUN npm install \
 && npm run build

# Stage 1: Only the compiled app, ready for production with Nginx
FROM nginx:1.15

COPY --from=build-stage /app/build/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
