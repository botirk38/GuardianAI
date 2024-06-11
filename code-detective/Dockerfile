FROM rust:latest

# Install dockerize
RUN apt-get update && apt-get install -y wget && \
  wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
  tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
  rm dockerize-linux-amd64-v0.6.1.tar.gz

# Create app directory
WORKDIR /app

# Copy the rest of the application code
COPY . /app

# Build the application
RUN cargo build --release

# Run the application using dockerize to wait for Kafka
ENTRYPOINT ["dockerize", "-wait", "tcp://kafka:9092", "-timeout", "60s", "./target/release/code-detective"]

