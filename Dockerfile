# Use a minimal Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
