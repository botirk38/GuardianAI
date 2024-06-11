
# Code Detective

Code Detective is a Rust-based tool designed to analyze Solana smart contracts for potential vulnerabilities. This service parses Rust code and identifies code patterns that may indicate security risks, such as overflows, underflows, reentrancy, and unauthorized access.

## Features

Code Detective extracts and identifies the following potential vulnerabilities:

- **Overflow Statements**: Detects possible overflow conditions in arithmetic operations.
- **Underflow Statements**: Detects possible underflow conditions in arithmetic operations.
- **Reentrancy Statements**: Identifies possible reentrancy vulnerabilities.
- **Authority Vulnerabilities**: Checks for missing authority checks on sensitive operations.
- **Signature Vulnerabilities**: Detects lack of signature verification on sensitive operations.
- **Frozen Account Modifications**: Ensures that sensitive operations are not performed on frozen accounts.
- **Structs, Enums, and Static Variables**: Collects information about structs, enums, and static variables in the code.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Rust
- Docker (for building and running the service in a container)

### Building and Running the Service

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/botirk38/GuardianAI
    cd code_detective
    ```

2. **Build the Docker Image**:
    ```sh
    docker build -t code_detective .
    ```

3. **Run the Docker Container**:
    ```sh
    docker run -p 8081:8081 code_detective
    ```

4. **Run Zookeeper**:
    ```sh
    zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
    ```

5. **Run Kafka**:
    ```sh
    kafka-server-start /opt/homebrew/etc/kafka/server.properties
    ```

### Usage

You can interact with the Code Detective service using a simple HTTP interface. Here's an example of how to use `curl` to analyze a piece of Rust code:

#### Example `curl` Request

```sh
curl -X POST http://localhost:8081/analyze_code -d '{
    "code": "
        pub fn transfer(&mut self, amount: u64) {
            if self.is_frozen() {
                panic!(\"Account is frozen\");
            }
            self.balance -= amount;
            if !self.invoke(amount) {
                panic!(\"Transfer failed\");
            }
        }
    "
}'
```

#### Then listen on the websocket for the response. Check out code-detective-model for more info.

### Code Structure

- **src/ast.rs**: Contains the AST parsing logic.
- **src/engine.rs**: Contains logic for detecting vulnerabilities.
- **src/tests/**: Contains tests for the service.

### Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contact

For any questions or support, please contact [your-email@example.com].


