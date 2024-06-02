

# API Gateway Vulnerability Detection

This project is a Spring Cloud Gateway application designed to route requests to various backend services, including a `code-detective` service. It uses OAuth2 for authentication and Redis for rate limiting.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Using Docker](#using-docker)
- [Endpoints](#endpoints)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Java 17 or later
- Gradle
- Docker (for running with Docker)
- Redis (if not using Docker)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo/api_gateway
    ```

2. Build the project:

    ```bash
    ./gradlew build -x test
    ```

## Configuration

### application.yml

Ensure the `application.yml` is properly configured. Below is a basic configuration:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: code-detective
          uri: http://localhost:8081
          predicates:
            - Path=/code-detective/{segment}
          filters:
            - StripPrefix=1

okta:
  oauth2:
    issuer: https://dev-az3di7fabdoc8vlz.uk.auth0.com/
    audience: https://safe-contracts/

server:
  port: 8080

logging:
  level:
    root: INFO
    org.springframework.cloud.gateway: DEBUG
    org.springframework.web: DEBUG
    reactor.netty: DEBUG

management:
  endpoints:
    web:
      exposure:
        include: '*'
  endpoint:
    health:
      show-details: always
```

### OAuth2 Configuration

Configure OAuth2 with your Okta credentials in the `application.yml` file.

## Running the Application

### Running Locally

1. Start the `code-detective` service (make sure it is running on `http://localhost:8081`).

2. Start the Spring Cloud Gateway:

    ```bash
    ./gradlew bootRun
    ```

### Using Docker

You can also run the application using Docker and Docker Compose.

1. Ensure you have Docker installed and running.

2. Build and run this server 

    ```bash
    cd ..
    docker build -t api_gateway_vuln_detection .
    ```
# Its highly recommended to run the docker compose at the root of the project




## Endpoints

- **Gateway Health Check:** `GET http://localhost:8080/actuator/health`
- **Code Detective Analyze Code:** `POST http://localhost:8080/code-detective/analyze_code`

## Troubleshooting

- **503 Service Unavailable:** Ensure the `code-detective` service is running and accessible. Verify the configurations in `application.yml` and ensure the services can communicate.

- **OAuth2 Issues:** Ensure your Okta OAuth2 configuration is correct and the issuer and audience values are properly set.


