# WindForLife POC
## Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout

### User
- `GET /api/user/profile/` - Get user profile
- `PUT /api/user/profile/` - Update user profile

### Wind Data
- `GET /api/wind/` - Get wind data
- `POST /api/wind/` - Add new wind data
- `PUT /api/wind/{id}/` - Update wind data
- `DELETE /api/wind/{id}/` - Delete wind data

## Running the Project

### Using Virtual Environment

1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Apply migrations:
    ```bash
    python manage.py migrate
    ```
5. Run the development server:
    ```bash
    python manage.py runserver
    ```

### Using Poetry

1. Install Poetry if you haven't already:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
2. Install dependencies:
    ```bash
    poetry install
    ```
3. Apply migrations:
    ```bash
    poetry run python manage.py migrate
    ```
4. Run the development server:
    ```bash
    poetry run python manage.py runserver
    ```

### Using Docker

1. Build the Docker image:
    ```bash
    docker build -t windforlife .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 windforlife
    ```

