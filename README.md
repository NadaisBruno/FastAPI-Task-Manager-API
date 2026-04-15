# FastAPI Task Manager API

**Live API:** [Open Swagger Docs](https://fastapi-task-manager-api-0rqu.onrender.com/docs)

A REST API built with FastAPI that allows users to manage their tasks and associated categories.
Includes authentication with JWT, task creation, deletion, and pagination as well as category management.
The API ensures that each user can only access their own data.

## Features

    - User registration
    - User login with JWT(JSON WEB Token) authentication
    - Password hashing with bcript algorithm
    - Create tasks
    - List tasks with pagination
    - Get a specifc task
    - Update tasks
    - Delete tasks
    - user-specific data access (security)
    - create categories
    - list categories with pagination


## Authentication Endpoints 

    - POST /register - Creates new users
    - POST /login - Login and get token for access
    - GET /me - Validates token and return the user email

## Task Endpoints

    - POST /tasks - Authenticated user can create specific tasks
    - GET /tasks - Paginated lists of tasks that belong to the authenticated user
    - GET /tasks/{task_id} - Retrieve a specific task by ID
    - PATCH /tasks/{task_id} - Update tasks fields by ID(title, description, completed)
    - DELETE //tasks/{task_id} - Delete tasks by ID

## Categories Endpoints

    - POST /categories - Creates new categories
    - GET /categories - Lists all categories with pagination


## How to run

1 - Start the server:

    uvicorn main:app --reload

2 - Open in your browser:

    http://127.0.0.1:8000/docs


## Technologies Used

    - Python >= 3.10
    - FastAPI
    - SQLAlchemy
    - Passlib (bcrypt)
    - python-jose(JWT)
    - Uvicorn