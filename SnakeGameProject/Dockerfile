# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /app
COPY . /app/

# Expose port 8000 to allow communication to/from server
EXPOSE 8000

# Run the Python script when the container launches
CMD ["python", "main.py"]
