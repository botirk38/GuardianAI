import pytest
import asyncio
import websockets
import jwt
from fastapi import HTTPException
from fastapi.testclient import TestClient
from httpx import AsyncClient
from ..websocket_server import app, validate_jwt_token, get_auth0_public_key

# Mock Auth0 public key and JWT validation
def mock_get_auth0_public_key():
    return {
        "kty": "RSA",
        "kid": "12345",
        "use": "sig",
        "n": "mock_n_value",
        "e": "AQAB"
    }

def mock_validate_jwt_token(token: str):
    if token == "valid_token":
        return {"sub": "1234567890"}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

# Patch the actual functions with the mocks
app.dependency_overrides[get_auth0_public_key] = mock_get_auth0_public_key
app.dependency_overrides[validate_jwt_token] = mock_validate_jwt_token

@pytest.mark.asyncio
async def test_websocket_valid_token():
    uri = "ws://localhost:8000/ws/test_client?token=valid_token"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello")
        response = await websocket.recv()
        print(f"Received: {response}")

@pytest.mark.asyncio
async def test_websocket_invalid_token():
    uri = "ws://localhost:8000/ws/test_client?token=invalid_token"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send("Hello")
            response = await websocket.recv()
            print(f"Unexpectedly received: {response}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed as expected: {e}")

@pytest.mark.asyncio
async def test_send_message():
    uri = "ws://localhost:8000/ws/test_client?token=valid_token"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello")
        response = await websocket.recv()
        print(f"Received: {response}")

        # Simulate sending a message from the server
        # This requires a direct call to the server method, which is not straightforward from a client script.
        # Instead, you can test it within the server using an internal mechanism.
        await app.send_message("test_client", "Message from queue")
        queue_message = await websocket.recv()
        assert queue_message == "Message from queue"
