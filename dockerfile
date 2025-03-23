# Use Python base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port (5000)
EXPOSE 8080

# Run Gunicorn server for Flask Web UI
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]