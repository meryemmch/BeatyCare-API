# syntax=docker/dockerfile:1

# Define Python version as an argument
ARG PYTHON_VERSION=3.13.0
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Create a user and switch to it
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt /app/

# Install dependencies (including uvicorn) from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Ensure that uvicorn is available in the PATH
RUN python -m pip show uvicorn

# Expose the port that the application listens on
EXPOSE 8000

# Run the application with uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
