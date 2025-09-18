# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including AutoDock Vina
RUN apt-get update && apt-get install -y --no-install-recommends \
    autodock-vina \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code into the container
COPY ./src/naturaDock/ /app/naturaDock/

# Specify the command to run on container start
ENTRYPOINT ["python", "-m", "naturaDock.main"]

