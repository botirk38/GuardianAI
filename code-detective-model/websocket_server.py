import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
import uvicorn
import jwt
import requests
from typing import Optional
from jose.backends import RSAKey, ALGORITHMS
from jose import jwt



app = FastAPI()

connected_clients = {}

# Auth0 configuration
AUTH0_DOMAIN = 'dev-az3di7fabdoc8vlz.uk.auth0.com'
AUTH0_AUDIENCE = 'your-auth0-audience'
ALGORITHM = 'RS256'

# Get the public key from Auth0
def get_auth0_public_key(token):
    # Extract the header from the token to find the key ID (kid)
    headers = jwt.get_unverified_header(token)
    kid = headers['kid']
    
    # Fetch the JWKS from Auth0
    json_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(json_url).json()
    
    # Find the key in JWKS
    rsa_key = next((key for key in jwks['keys'] if key['kid'] == kid), None)
    if rsa_key:
        public_key = RSAKey(rsa_key, ALGORITHMS.RS256)
        return public_key
    else:
        raise Exception("Public key not found.")
# Validate JWT token
def validate_jwt_token(token: str):
    try:
        # Assuming you already have the RSA public key obtained and converted
        public_key = get_auth0_public_key(token)
        # Decode the token
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM], audience=AUTH0_AUDIENCE)
        return payload
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, token: Optional[str] = Query(None)):
    if token is None:
        await websocket.close(code=1008)
        print(f"Connection closed for {client_id}: No token provided")
        return

    try:
        payload = validate_jwt_token(token)
        await websocket.accept()
        connected_clients[client_id] = websocket
        try:
            while True:
                data = await websocket.receive_text()
                print(f"Received message from {client_id}: {data}")
        except WebSocketDisconnect:
            print(f"Client {client_id} disconnected")
            del connected_clients[client_id]
    except HTTPException as e:
        await websocket.close(code=1008)
        print(f"Connection closed for {client_id}: {e.detail}")

async def send_message(client_id: str, message: str):
    if client_id in connected_clients:
        websocket = connected_clients[client_id]
        await websocket.send_text(message)

async def start_websocket_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    print("Starting server at http://0.0.0.0:8000")
    await server.serve()

if __name__ == "__main__":
    asyncio.run(start_websocket_server())
