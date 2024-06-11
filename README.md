

# Project: Safe Contracts API

Safe Contracts is a tool that analyzes smart contracts for security vulnerabilities. It uses static analysis to detect common security issues in Solana code. The tool is accessible through an API that can be used to analyze smart contracts programmatically.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running with Docker Compose](#running-with-docker-compose)
- [Calling the API](#calling-the-api)
- [Using the Extension](#using-the-extension)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/botirk38/GuardianAI.git
    cd your-repo
    ```

## Running with Docker Compose

To build and run the services using Docker Compose, follow these steps:

1. **Navigate to the root directory of the project:**


2. **Build and run the containers:**

     ```bash
    docker-compose -f docker-compose.yml up  --build

    ```

This will start the Spring Cloud Gateway on `http://localhost:8080` and the `code-detective` service on `http://localhost:8081`.

## Calling the API

You can interact with the `code-detective` service through the API Gateway.

### Authentication
```bash
curl --request POST \
  --url https://dev-az3di7fabdoc8vlz.uk.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"your_client_id","client_secret":"your_client_secret","audience":"https://safe-contracts/","grant_type":"client_credentials"}'

```

Replace `your_client_id` and `your_client_secret` with your Auth0 client ID and client secret, that can be obtained from the Auth0 dashboard.

### Direct API Call

To call the `analyze_code` endpoint directly, use the following curl command:

```bash
curl -X POST http://localhost:8080/code-detective/analyze_code \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"code": "your code here"}'
```

Replace `YOUR_JWT_TOKEN` with a valid JWT token and `{"code": "your code here"}` with the appropriate payload for your request.

### Using the Extension

You can also use the Safe Contracts Vscode extension that interacts with the API Gateway to analyze your code for vulnerabilities. The extension is available in the `smartguardian` directory.

## Troubleshooting

- **503 Service Unavailable:** Ensure that both the Spring Cloud Gateway and `code-detective` service are running. Verify that the services can communicate within the Docker network.

- **OAuth2 Issues:** Ensure your Okta OAuth2 configuration is correct in the `application.yml` file of the `api_gateway` service. Verify that the issuer and audience values are properly set.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

