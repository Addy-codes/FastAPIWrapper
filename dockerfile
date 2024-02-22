# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Copy the requirements file from your host to your current location.
# COPY requirements.txt .

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of your app's source code from your host to your image filesystem.
# COPY ./app ./app

# # Make sure to set the PYTHONPATH environment variable if necessary
# ENV PYTHONPATH=/usr/src/app

# # Run the application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install wget to download the file
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Download interactsh-client from Google Drive
RUN wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1xfzYMC23Gd1LBwXoMh907UEMxTo-ekm2' -O interactsh-client && \
    chmod +x interactsh-client && \
    mv interactsh-client /usr/local/bin/

# Copy the requirements file from your host to your current location.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY ./app ./app

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Ensure the container is using UTF-8 encoding by default
ENV LANG C.UTF-8

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
