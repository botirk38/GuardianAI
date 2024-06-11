FROM python:3.9

# Install your dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install dockerize
RUN apt-get update && apt-get install -y wget && \
  wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
  tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
  rm dockerize-linux-amd64-v0.6.1.tar.gz

# Copy your application code
COPY . /app
WORKDIR /app

# Run the application using dockerize to wait for Kafka
ENTRYPOINT ["dockerize", "-wait", "tcp://kafka:9092", "-timeout", "60s", "python", "main.py"]

