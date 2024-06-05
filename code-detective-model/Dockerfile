# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 50051 available to the world outside this container
EXPOSE 50051

# Define environment variable for OpenAI API Key
ENV OPENAI_API_KEY=your_openai_api_key_here

# Run the application
CMD ["python", "open_ai_service_server.py"]
