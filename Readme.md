# FastApi Task Manager API

A REST API app built with FastAPI that allows users to manage their tasks.
Includes authentication with JWT, task creation, deletion, and pagination.
The API ensures that each user can only access their own tasks.

## Features

    - User registration
    - User login with JWT(JSON WEB Token) authentication
    - Password hashing with bcript algoritm
    - Create tasks
    - List tasks with pagination
    - Get a specifc task
    - Update tasks
    - Delete tasks
    - user-specific data access (security)


## Task Endpoints 

    - POST /register - Creates new users
    - POST /login - Login and get token for access
    - GET /me - Validates token and return the user email

## Authentication Endpoints

    - POST /Tasks - Authenticated user can create specific tasks
    - GET /Tasks - Paginated lists of tasks that belong to the authenticated user
    - GET /tasks/{task_id} - Retrive a specific task by ID
    - PATCH /tasks/{task_id} - Update tasks fields by ID(title, description, completed)
    - DELETE //tasks/{task_id} - Delete tasks by ID


## How to run

1 - Start thr server:

    uvicorn main:app --reload

2 - Open in your browser:

    http://127.0.0.1:8000/docs


## Tecnologies Used

    - Python >= 3.10
    - FastAPI
    - SQAlquemy
    - Passlib (bcrypt)
    - python-jose(JWT)
    - Uvicorn