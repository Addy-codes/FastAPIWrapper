
# FastAPI Wrapper

This project provides a FastAPI wrapper around the Interactsh tool, offering an easy-to-use API interface for generating URLs for out-of-band (OOB) interaction testing and retrieving interaction logs. The service is containerized using Docker, simplifying deployment and execution.

## Features

- **Generate OOB URLs**: Easily generate unique URLs for OOB testing with Interactsh.
- **Fetch Interactions**: Retrieve detailed logs of interactions, including caller IP and timestamps, optionally filtered by time range.

## Requirements

- Docker
- Docker Compose

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Setup with Docker

1. **Clone the Repository**

   Start by cloning this repository to your local machine:

   ```bash
   git clone https://github.com/Addy-codes/FastAPIWrapper
   cd FastAPIWrapper
   ```

2. **Build and Run with Docker Compose**

   Use Docker Compose to build and run the application:

   ```bash
   docker-compose up --build
   ```

   This command builds the Docker image and starts the service. The API will be accessible at `http://127.0.0.1/docs`.

### API Endpoints

- **GET `/api/getURL`**: Generates and returns a unique URL for OOB testing.
- **GET `/api/getInteractions`**: Retrieves interaction logs for the specified URL. Supports optional query parameters for start and end timestamps to filter interactions within a specific time range.

### Accessing the API Documentation

FastAPI generates interactive API documentation using Swagger UI. Once the application is running, you can visit `http://127.0.0.1/docs` in your web browser to access the documentation, try out the API endpoints, and view their responses.

## Screenshots and steps to run the API:

![image](https://github.com/Addy-codes/FastAPIWrapper/assets/72205091/f8d4a52c-665f-4c6b-937b-a9775cd6c9f8)

- Get the url from getURL endpoint:

![image](https://github.com/Addy-codes/FastAPIWrapper/assets/72205091/3bad9e98-0c9d-4010-8150-51f37ceb663b)

- Copy the url and paste it in the browser to interact with it:

![image](https://github.com/Addy-codes/FastAPIWrapper/assets/72205091/a93489c3-0a61-48c1-9571-b9d843718e93)

- Interactions can be viewed using the getInteractions endpoint (make sure to paste the above generated url).
  
- Note: Browsers automatically request additional resources like /favicon.ico after loading the main page. This behavior explains why you see multiple entries for what seems like a single interaction. When a user visits a website, the browser often makes several requests behind the scenes:

![image](https://github.com/Addy-codes/FastAPIWrapper/assets/72205091/e47b4351-2093-4842-aece-58d3c140fdfd)

- You can also filter the interactions using timestamps:

![image](https://github.com/Addy-codes/FastAPIWrapper/assets/72205091/4fbbc17c-7884-45ca-a074-52200dc6bdb5)


## Development

To modify the application or add new features, you can edit the Python files located in the project directory. The main components are:

- `app/main.py`: FastAPI application setup and route inclusion.
- `app/routes.py`: API route definitions.
- `app/utils.py`: Utility functions for interacting with Interactsh and processing data.
