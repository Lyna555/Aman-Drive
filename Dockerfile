# Use official Python image
FROM python:3.8.6

# Set working directory in container
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your app runs on (optional, good practice)
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
