# Use the official Rust image as the base image for building
FROM rust:latest as builder

# Install dependencies required for protobuf and gRPC
RUN apt-get update && \
  apt-get install -y \
  protobuf-compiler \
  libprotobuf-dev \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /usr/src

# Copy the entire project directory into the container
COPY . .

# Build the project in release mode
RUN cargo build --release

# Run the tests
RUN cargo test --release

# Stage 2: Use the same base image as the build stage to avoid GLIBC version issues
FROM rust:latest

# Set the working directory inside the container
WORKDIR /usr/local/bin

# Copy the compiled binary from the builder stage
COPY --from=builder /usr/src/target/release/code-detective .

# Expose the port on which the gRPC service will run
EXPOSE 8081

# Command to run the binary
CMD ["./code-detective"]

