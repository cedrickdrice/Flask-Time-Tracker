# Flask Time Tracker Project

## Overview

Flask Time Tracker is a web-based application for tracking time spent on various projects. It allows users to time-in and time-out and view their weekly work summary.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: The application is containerized with Docker, making it easy to set up and run regardless of your environment.

## Installing Docker

Follow the instructions below to install Docker:

### Windows:

1. Download Docker Desktop from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. Follow the installation instructions for your operating system.
3. Once installed, launch Docker Desktop.

## Running the Application
Once Docker is installed, you can run the Flask Time Tracker application as follows:

1. Clone the repository (if you haven't already):

   ```bash
   git clone https://github.com/cedrickdrice/time-tracker.git
   cd timetracker
   
2. Build and run the application using Docker Compose: (This command builds the Docker image and starts the containers defined in docker-compose.yml.)
    ```bash
   docker-compose up --build
   
3. Once the containers are running, you can access the application at http://localhost:5000.

## Stopping the Application
To stop the application, use the following command:
```bash
docker-compose down
```

## Project Information
- Application Structure: The Flask application is structured with models, routes, and services.
- Database: The application uses SQLite for data storage.

--------------------------------

# API Documentation

This section outlines the various API endpoints available in the Flask Time Tracker application, detailing their purpose and usage.

## Authorization
All API requests require an API key for authentication. The API key should be included in the Authorization header of each request.

```bash
Authorization: Bearer YOUR_API_KEY
```

## Signup

### `POST /api/signup`

* **Description**: Signup a new user to the application.
* **Request Body**:

  | Parameter | Type | Description |
  | :--- | :--- | :--- |
  | `username` | `string` | **Required**. User's desired username. |
  | `email` | `string` | **Required**. User's email address. |
  | `password` | `string` | **Required**. User's chosen password. |
  
  ```json
  {
    "username" : "cediedrice12",
    "email" : "cediedrice@gmail12.com",
    "password" : "123456"
  }
  ```

* **Response**: Returns a success message upon successful signup or an error message on failure.

## Login

### `POST /api/login`

* **Description**: Authenticate a user and return an access token.
* **Request Body**:

  | Parameter | Type | Description |
    | :--- | :--- | :--- |
  | `username` | `string` | **Required**. User's username. |
  | `password` | `string` | **Required**. User's password. |
  ```json
  {
    "username" : "cediedrice12",
    "password" : "123456"
  }
  ```
* **Response**: On successful authentication, returns an access token for the user. On failure, returns an error message.

## Time Entry

### `POST /api/time`

* **Description**: Record a user's time-in (start of a work session).
* **Request Body**:

  | Parameter | Type     | Description                                             |
      |:---------|:--------------------------------------------------------| :--- |
  | `project` | `int`    | **Required**.  ID of the project the time entry is for. |
  | `description` | `string` | **Required**. Description of the work session.          |

  ```json
  {
    "project" : "2",
    "description" : "123456"
  }
  ```

* **Response**: Returns a success message upon successful time entry or an error message if the user has already timed in.

    ```json
        {
            "code": 200,
            "message": "Time Registered Successfully",
            "data": {
                "id": 2,
                "email": "cediedrice@gmail.com",
                "username": "cediedrice",
                "exp": 1700334394
            }
    }
    ```

### `PUT /api/time`

* **Description**: Record a user's time-out (end of a work session).
* **Response**: Returns a success message upon successful time-out or an error message if the user has already timed out for the day.

    ```json
    {
        "code": 200,
        "message": "Timeout Registered Successfully"
    }
    ```    

## Work Summary

### `GET /api/work`

* **Description**: Retrieve the user's weekly work summary.
* **Response**: Returns a summary of the total hours worked by the user on each project for the current week.
    ```json
	  {
		    "code": 200,
		    "message": "User Week Summary for the 45th week: 2023-11-12",
		    "data": [
		        {
		            "project": "Project 1",
		            "total_hours": 24.0
		        },
		        {
		            "project": "Project 2",
		            "total_hours": 3.03
		        }
		    ]
		}
    ```    

## Testing the API
The **api_test.sh** script is provided to test the API endpoints for user signup and login. Follow these steps to run the tests:

### Prerequisites for Testing
On Windows, use Git Bash or a similar environment to run the script.

### Running the Tests
1. Navigate to the directory containing your Flask Time Tracker project.
2. Make sure your Flask application is running.
3. To execute the tests, run the following command in your terminal:
``` bash
./api_test.sh
```