# TODO App with FastAPI and MongoDB

A simple TODO application built with FastAPI and MongoDB database.

## Features

- ✅ Create a new task
- ✅ Get all tasks
- ✅ Get a specific task by ID
- ✅ Update a task
- ✅ Delete a task
- ✅ CORS enabled for cross-origin requests
- ✅ Automatic API documentation with Swagger UI

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account or local MongoDB installation
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd mongodb
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: install Streamlit frontend dependencies for local UI use:**
   ```bash
   pip install streamlit==1.28.1 requests==2.31.0
   ```

5. **Configure MongoDB Connection:**
   - Open `.env` file
   - Replace `your_username`, `your_password`, and `your_cluster` with your MongoDB Atlas credentials
   - Example:
     ```
     MONGODB_URL=mongodb+srv://user:password@cluster0.mongodb.net/?retryWrites=true&w=majority
     ```

## Usage

1. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at: `http://localhost:8000`

2. **Access API Documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Create Task
- **Endpoint:** `POST /tasks`
- **Body:**
  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, eggs, and bread",
    "completed": false
  }
  ```
- **Response:** Created task with ID and timestamps

### 2. Get All Tasks
- **Endpoint:** `GET /tasks`
- **Response:** List of all tasks

### 3. Get Task by ID
- **Endpoint:** `GET /tasks/{task_id}`
- **Response:** Specific task details

### 4. Update Task
- **Endpoint:** `PUT /tasks/{task_id}`
- **Body:**
  ```json
  {
    "title": "Updated title",
    "description": "Updated description",
    "completed": true
  }
  ```
- **Response:** Updated task

### 5. Delete Task
- **Endpoint:** `DELETE /tasks/{task_id}`
- **Response:** 204 No Content (Success)

## Deployment on Vercel

### Prerequisites
- Vercel account (https://vercel.com)
- GitHub repository connected to Vercel
- MongoDB Atlas account with connection string

### Steps to Deploy

1. **Set Environment Variables on Vercel:**
   - Go to Vercel Dashboard → Project Settings → Environment Variables
   - Add the following variables:
     ```
     MONGODB_URL = your_mongodb_connection_string
     DATABASE_NAME = todo_db (or your chosen name)
     COLLECTION_NAME = tasks (or your chosen name)
     ```

2. **Ensure MongoDB Connection String is Secure:**
   - Use Vercel's Environment Variables (never commit `.env` to git)
   - Example connection string format:
     ```
     mongodb+srv://username:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority
     ```

3. **Deploy:**
   - Push your changes to GitHub
   - Vercel will automatically detect and deploy
   - Your API will be available at: `https://your-project.vercel.app/`

4. **Test the Deployment:**
   - API Health Check: `https://your-project.vercel.app/health`
   - Swagger UI: `https://your-project.vercel.app/docs`
   - API Root: `https://your-project.vercel.app/`

### Important Notes
- Only the FastAPI backend is deployed on Vercel
- `requirements.txt` intentionally contains backend-only dependencies so Vercel does not try to install Streamlit-only packages during deployment
- The Streamlit frontend should be run locally or deployed separately on Streamlit Cloud, with `streamlit` and `requests` installed manually
- For production, update the `STREAMLIT_API_URL` environment variable to point to your Vercel API
- The API has CORS enabled for all origins (you may want to restrict this in production)

## Project Structure

```
mongodb/
├── main.py              # FastAPI application and routes
├── models.py            # Pydantic models for request/response
├── database.py          # MongoDB connection and setup
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md           # This file
```

## Example Usage with cURL

```bash
# Create a task
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Study FastAPI with MongoDB",
    "completed": false
  }'

# Get all tasks
curl -X GET "http://localhost:8000/tasks"

# Get task by ID
curl -X GET "http://localhost:8000/tasks/YOUR_TASK_ID"

# Update a task
curl -X PUT "http://localhost:8000/tasks/YOUR_TASK_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task",
    "completed": true
  }'

# Delete a task
curl -X DELETE "http://localhost:8000/tasks/YOUR_TASK_ID"
```

## MongoDB Connection Issues?

If you can't connect to MongoDB:

1. **Check your MongoDB Atlas cluster is active**
2. **Verify network access:** Whitelist your IP in MongoDB Atlas
3. **Check credentials:** Ensure username and password are correct
4. **For local MongoDB:** Use `mongodb://localhost:27017`

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server to run FastAPI
- **PyMongo** - Python driver for MongoDB
- **Pydantic** - Data validation using Python types
- **python-dotenv** - Load environment variables from .env file

## License

MIT License
