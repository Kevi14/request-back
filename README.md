markdown
Copy code

# Project Documentation

This project is containerized using Docker, providing a consistent development and deployment environment.

## Quick Commands

- **Testing**:
  docker-compose run test

- **Development Server**:
  docker-compose up web

- **Production Server**:
  docker-compose up web-prod

## Project Structure:

The names of the folders are self-descriptive

- `middlewares/`
- `routes/`
- `tests/`
- `models/`

The **init**.py of the app folder holds the starting point of the application where the orm , routes and the others are embeded in the flask app
