# Skillect

A Client-Server website, meant to store and display experiences and skills.

## How to use

One need `docker` and `docker-compose` to start the application.

Run `make`

## Development

During development, use `make dev`.

It starts
- The frontend development server, serving the frontend pages with a live reload on [`http://localhost:3000`](http://localhost:3000)
- The backend server, with a live reload of the scripts at [`http://localhost:5000`](http://localhost:5000)
  - [`http://localhost:5000/docs`](http://localhost:5000/docs) offers **Swagger** webpage
  - [`http://localhost:5000/redoc`](http://localhost:5000/redoc) offers **ReDoc** webpage
