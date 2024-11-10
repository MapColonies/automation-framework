# Use an official Python runtime as the base image -  if need upgrade to 3.12 or newer
FROM python:3.9-slim

# Set environment variables to ensure Python runs in unbuffered mode and does not create .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements file to the container
COPY ../requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project directory into the container
COPY .. /app

# Install pre-commit hooks
RUN pip install pre-commit && pre-commit install

# Command to run the tests when the container starts
CMD ["pytest", "src/tests", "--html=reports/report.html", "--self-contained-html"]
