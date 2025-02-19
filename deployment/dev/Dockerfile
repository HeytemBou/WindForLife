# Use official Python image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the project files
COPY ../pyproject.toml ../poetry.lock /app/
COPY .. /app/

# Install dependencies using Poetry
RUN poetry install --verbose && poetry shell


# Expose port 8000 (default Django port)
EXPOSE 8000

# Run Django development server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
