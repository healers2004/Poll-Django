# Use the official Python image from the Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Run migrations and collect static files
RUN python manage.py migrate

# Install gunicorn
RUN pip install gunicorn

# Expose port 8000 to the host
EXPOSE 8000

# Start the Django application using gunicorn
CMD python manage.py runserver