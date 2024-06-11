from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
import uvicorn

app = FastAPI()

connected_clients = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connected_clients[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from {client_id}: {data}")
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
        del connected_clients[client_id]


async def send_message(client_id: str, message: str):
    if client_id in connected_clients:
        websocket = connected_clients[client_id]
        await websocket.send_text(message)


async def start_websocket_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
