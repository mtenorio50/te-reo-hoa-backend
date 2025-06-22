# Use official Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies needed for your app and for zstd/tar
RUN apt-get update && apt-get install -y --no-install-recommends \
    zstd \
    tar \
    gcc \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy all files from your project into the container
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8080 (fly.io standard, matches uvicorn below)
EXPOSE 8080

# Command to run your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
