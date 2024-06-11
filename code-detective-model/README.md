# Code Detective Model 

Code-Detective model is the AI engine that detects vulnerabilites within smart contract code for Solana.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [File Structure](#file-structure)
7. [Contributing](#contributing)
8. [License](#license)

## Overview
GuardianAI Smart Contract Vulnerability Detection Service allows users to analyze Rust smart contract code for potential vulnerabilities. The service uses Kafka for processing requests and WebSockets for real-time communication with clients.

## Features
- **Real-time Analysis**: Uses WebSockets to provide real-time responses to clients.
- **Asynchronous Processing**: Utilizes `aiokafka` and FastAPI for efficient, non-blocking operations.
- **Scalable**: Designed to handle multiple concurrent connections and requests.
- **Extensible**: Easily extendable to add more features or integrate with other systems.

## Architecture
The service consists of three main components:
1. **WebSocket Server**: Handles client connections and maintains persistent connections using FastAPI.
2. **Kafka Consumer**: Processes incoming messages from Kafka, analyzes the smart contract code, and sends results back to clients.
3. **Main Application**: Coordinates the WebSocket server and Kafka consumer to run concurrently.

## Setup and Installation

### Prerequisites
- Python 3.8+
- Kafka server running locally or accessible remotely
- `pip` package manager

### Installation Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/guardianai-vulnerability-detection.git
   cd guardianai-vulnerability-detection
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Ensure Kafka is running and accessible.
   - Set up your OpenAI API key in your environment variables or a configuration file.

## Usage

### Running the Service
1. **Start the WebSocket Server and Kafka Consumer**
   ```sh
   python3 main.py
   ```

### Client Connection
Clients can connect to the WebSocket server using the following URL format:
```
ws://0.0.0.0:8000/ws/{client_id}


```

Replace `{client_id}` with a unique identifier for each client.

### Example Client Code (JavaScript)
```javascript
const clientId = '12345';
const websocket = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

websocket.onopen = function() {
    console.log('WebSocket connection established');
    websocket.send(JSON.stringify({ request_id: clientId, message: 'Hello, server!' }));
};

websocket.onmessage = function(event) {
    console.log('Message from server:', event.data);
};

websocket.onclose = function() {
    console.log('WebSocket connection closed');
};

websocket.onerror = function(error) {
    console.log('WebSocket error:', error);
};
```

## File Structure
```
project/
│
├── websocket_server.py
├── kafka_consumer.py
└── main.py
```

- **`websocket_server.py`**: Handles WebSocket connections using FastAPI.
- **`kafka_consumer.py`**: Consumes messages from Kafka, processes them, and communicates with WebSocket clients.
- **`main.py`**: Coordinates the WebSocket server and Kafka consumer to run concurrently.

## Contributing
We welcome contributions to improve the service. Please fork the repository and submit pull requests for review.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

