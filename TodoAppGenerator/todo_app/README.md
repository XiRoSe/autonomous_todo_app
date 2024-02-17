
# ToDo Application

## Overview
This is a simple ToDo application with a FastAPI backend and a SQLite database.

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy

## Installation
Install the required packages using pip:

```bash
pip install -r requirements.txt
Running the Application
Start the application with Uvicorn:

bash
Copy code
uvicorn app.main:app --reload
API Endpoints
Create a new ToDo item: POST /todo/
Get all ToDo items: GET /todo/
Get a single ToDo item by ID: GET /todo/{todo_id}
Update a ToDo item by ID: PUT /todo/{todo_id}
Delete a ToDo item by ID: DELETE /todo/{todo_id}
