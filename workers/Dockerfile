# Base image for Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the default command for the container
CMD ["celery", "-A", "cel_main", "worker", "--loglevel=info"]
