# P-ToDo-Y: Mahasiswa API with Clean Architecture

This project implements a RESTful API for managing Mahasiswa (Student) data, built with Python, FastAPI, and SQLAlchemy, following the principles of Clean Architecture.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Database Management](#database-management)
  - [Migrations (Alembic)](#migrations-alembic)
  - [Seeding (Data Faker)](#seeding-data-faker)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## About
P-ToDo-Y is designed as a clear demonstration of how to structure a Python application using Clean Architecture. It provides core CRUD operations for `Mahasiswa` (Student) entities, showcasing separation of concerns, dependency inversion, and testability.

## Features
*   **Mahasiswa CRUD:** Create, Read, Update, and Delete student records.
*   **Clean Architecture:** Clear separation into Domain, Use Case, Ports, Infrastructure, and Repository layers.
*   **FastAPI:** High-performance web framework for building APIs.
*   **SQLAlchemy ORM:** Database interaction using an Object-Relational Mapper.
*   **Alembic Migrations:** Manage database schema evolution.
*   **Data Seeding:** Populate the database with realistic fake data using `Faker`.
*   **Pydantic/Dataclasses for DTOs:** Strict data validation and clear data contracts.
*   **Dependency Injection:** Managed through FastAPI's dependency system.

## Architecture
The project adheres to Clean Architecture principles, organizing code into distinct layers:

```
P-ToDo-Y/
├── src/
│   ├── application/               # Application Core (Business Logic)
│   │   ├── domains/               # Business Entities (Mahasiswa, BaseEntity)
│   │   ├── dtos/                  # Data Transfer Objects (MahasiswaDto, CreateMahasiswaDto, etc.)
│   │   └── usecases/              # Application-specific business rules
│   │       ├── interfaces/        # Interfaces/Abstract classes for external dependencies (e.g., repositories)
│   │       └── mahasiswa.py       # MahasiswaService (interactors/use cases)
│   ├── config.py                  # Environment/Application configuration
│   ├── dependencies.py            # Centralized FastAPI dependencies (e.g., get_mahasiswa_service)
│   ├── infrastructure/            # Frameworks and external services
│   │   ├── app.py                 # FastAPI application setup, main entry point
│   │   └── routes.py              # API endpoint definitions (FastAPI routers)
│   ├── ports/                     # Data contracts/APIs for external services (e.g., GetMahasiswaPort)
│   └── repositories/              # Data persistence (database, external APIs)
│       └── database/              # SQLAlchemy-specific implementation
│           ├── core.py            # SQLAlchemy engine, session management, Base class
│           ├── models/            # SQLAlchemy ORM models
│           └── mahasiswa.py       # Concrete MahasiswaRepository implementation
├── alembic/                       # Alembic migration scripts
├── alembic.ini                    # Alembic configuration
├── .env                           # Environment variables
├── manage.py                      # Management script for seeding, etc.
└── requirements.txt               # Project dependencies
```

## Prerequisites
Before you begin, ensure you have the following installed:
*   Python 3.8+
*   pip (Python package installer)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/P-ToDo-Y.git
    cd P-ToDo-Y
    ```

2.  **Create and activate a virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
The project uses a `.env` file for environment-specific configurations, such as the database URL.

1.  **Create a `.env` file:**
    In the root directory of your project, create a file named `.env`.

2.  **Add database configuration:**
    Add your database connection string to this file. For development, a SQLite database is used by default.

    ```dotenv D:\Kuliah\Sem 5\PMPL\P-ToDo-Y\.env
    DB_URL="sqlite:///./mahasiswa.db"
    ```
    If you're using a different database (e.g., PostgreSQL, MySQL), update the `DB_URL` accordingly (e.g., `DB_URL="postgresql://user:password@host:port/database_name"`).

## Database Management

### Migrations (Alembic)
Alembic is used for managing database schema changes.

1.  **Initialize Alembic (if not already done):**
    ```bash
    alembic init alembic
    ```
    *(This has likely been done during setup, creating the `alembic/` directory and `alembic.ini`)*

2.  **Configure `alembic/env.py`:**
    The `alembic/env.py` file has been configured to read your project's `Config` and `Base.metadata`. Ensure your `alembic/env.py` matches the provided structure.

3.  **Generate a new migration script:**
    Whenever you make changes to your SQLAlchemy models (e.g., add a new field, create a new model), generate a new migration script:
    ```bash
    alembic revision --autogenerate -m "Description of your changes"
    ```
    This will create a new Python file in `alembic/versions/`. **Always review this file** to ensure it accurately reflects your intended schema changes.

4.  **Apply migrations to the database:**
    To execute the schema changes defined in your migration scripts:
    ```bash
    alembic upgrade head
    ```
    This command applies all pending migrations up to the latest one (`head`).

### Seeding (Data Faker)
Use the `manage.py` script to populate your database with initial, fake data.

1.  **Run the seeder:**
    ```bash
    python manage.py seed
    ```
    This command will generate 10 fake `Mahasiswa` records with realistic NIMs (prefixed by the current year) and class formats, then insert them into your database. It automatically checks for existing NIMs to prevent duplicate entries if run multiple times. You can adjust the number of generated records in `manage.py`.

## Running the Application
Once the database is set up and (optionally) seeded, you can start the FastAPI application using Uvicorn.

```bash
uvicorn src.infrastructure.app:app --reload
```
*   `src.infrastructure.app:app`: Points Uvicorn to your FastAPI application instance.
*   `--reload`: Automatically reloads the server on code changes (useful for development).

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

You can access the FastAPI interactive documentation (Swagger UI) at `http://127.0.0.1:8000/docs` to test the endpoints.

### Mahasiswa Endpoints (`/mahasiswa`)

*   **`POST /mahasiswa/`**: Create a new Mahasiswa record.
    *   **Request Body:** `CreateMahasiswaDto`
    *   **Response:** `MahasiswaDto` (HTTP 201 Created)
*   **`GET /mahasiswa/`**: Retrieve a list of Mahasiswa records.
    *   **Query Parameters:** `id`, `nim`, `nama`, `kelas`, `tempat_lahir`, `tanggal_lahir` (YYYY-MM-DD), `order_by`, `order` (asc/desc), `limit`, `page` (all optional for filtering and pagination).
    *   **Response:** `list[MahasiswaDto]`
*   **`PUT /mahasiswa/{mahasiswa_id}`**: Update an existing Mahasiswa record.
    *   **Path Parameter:** `mahasiswa_id` (int)
    *   **Request Body:** `CreateMahasiswaDto` (note: for simplicity, `CreateMahasiswaDto` is reused; a dedicated `UpdateMahasiswaInputDto` is recommended for production)
    *   **Response:** `MahasiswaDto`
*   **`DELETE /mahasiswa/{mahasiswa_id}`**: Delete a Mahasiswa record.
    *   **Path Parameter:** `mahasiswa_id` (int)
    *   **Response:** No Content (HTTP 204 No Content)

## Contributing
Feel free to fork the repository, make improvements, and submit pull requests.

## License
This project is licensed under the MIT License.
