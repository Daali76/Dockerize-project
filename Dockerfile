# Use the official Python image as the base image
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the working directory
COPY . .

# Expose the port on which the Flask app will run
# Run the Flask app when the container starts
CMD ["gunicorn", "api:app", "--bind", "0.0.0.0:8000" ]