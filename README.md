# P-ToDo-Y: Mahasiswa API with Clean Architecture

## What This Is

P-ToDo-Y is a RESTful API for managing Mahasiswa (Student) data, built with Python, FastAPI, and SQLAlchemy. It demonstrates Clean Architecture principles with a clear separation of concerns, dependency injection, and testable code structure. The API provides core CRUD operations for student records with proper data validation using Pydantic DTOs.

## Developer Guide

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your_username/P-ToDo-Y.git
   cd P-ToDo-Y
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Create a `.env` file in the root directory.
2. Configure your database connection (SQLite is used by default):
   ```
   DB_URL="sqlite:///./mahasiswa.db"
   ```
   For other databases like PostgreSQL, use:
   ```
   DB_URL="postgresql://user:password@host:port/database_name"
   ```

## Running Guide

### Database Setup
1. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

2. Seed the database with sample data (optional):
   ```bash
   python manage.py seed
   ```

### Start the Application
Run the FastAPI application using Uvicorn:
```bash
uvicorn src.infrastructure.app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Documentation
Access the interactive documentation (Swagger UI) at:
`http://127.0.0.1:8000/docs`

The API provides the following endpoints:
- `POST /mahasiswa/`: Create a new Mahasiswa record
- `GET /mahasiswa/`: Retrieve Mahasiswa records with filtering and pagination
- `PUT /mahasiswa/{mahasiswa_id}`: Update a Mahasiswa record
- `DELETE /mahasiswa/{mahasiswa_id}`: Delete a Mahasiswa record