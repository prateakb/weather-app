# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port
EXPOSE 5000

WORKDIR /app/weather_api

# Run the command to start the application
CMD /bin/bash -c "gunicorn -b 0.0.0.0:5000 wsgi:app"
