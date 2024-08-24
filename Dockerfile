# Use the official Python image as a base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /code

# Install dependencies
COPY requirements /code/requirements
RUN pip install -r /requirements/docker.txt

# Copy the rest of the application code
COPY . /code/

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
