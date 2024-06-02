# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Gradle wrapper and the build files
COPY gradle /app/gradle
COPY gradlew /app
COPY build.gradle /app
COPY settings.gradle /app

# Copy the source code
COPY src /app/src

# Download the project dependencies
RUN ./gradlew dependencies

# Build the project
RUN ./gradlew build -x test

# Expose the port that the application will run on
EXPOSE 8080

# Command to run the application
CMD ["java", "-jar", "build/libs/api-gateway-vuln-detection-0.0.1-SNAPSHOT.jar"]
