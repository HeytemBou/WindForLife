# WindForLife POC

## Endpoints served by DRF in this project
### Authentication
- `POST /api/v1/sign-up/` 
- `POST /api/v1/sign-in/` 

### Anemometers
- `GET /api/v1/anemometers/`
- `POST /api/v1/anemometers/`
- `PUT /api/v1/anemometers/<id>`
- `DELETE /api/v1/anemometers/<id>`
- `POST /api/v1/anemometers/<id>/measurements`
- `GET /api/v1/anemometers/<id>/measurements`

### Measurements
- `GET /api/v1/measurements/wind-speed-stats`
- `GET /api/v1/measurements/filter-by-tags`
- `GET /api/v1/measurements/stats-within-area`

## Testing
For testing these endpoints locally, you can import the provided postman collection in the folder postman-colletion.

## Running the Project
### Using Poetry

1. Install Poetry if you haven't already:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
2. Install dependencies:
    ```bash
    poetry install
    ```
3. Activate the env
    ```bash
    poetry shell
    ```
4. Apply migrations:
    ```bash
    python manage.py migrate
    ```
5. Run the development server:
    ```bash
    python manage.py runserver
    ```

### Using Docker

1. Build the Docker image:
    ```bash
    docker build -t deployment/dev/ .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 windforlifePOC
    ```

