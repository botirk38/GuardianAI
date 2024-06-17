import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
import asyncio

app = FastAPI()

connected_clients = {}

predefined_messages = [
    "Hello from the server!",
    "How are you today?",
    "This is a test message.",
    "Goodbye!"
]


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, token: str):
    if token == "1090":
        await websocket.accept()
        print(f"Client {client_id} connected with token: {token}")
        connected_clients[client_id] = websocket
        try:
            for message in predefined_messages:
                await websocket.send_text(f"Server says: {message}")
                await asyncio.sleep(2)
        except WebSocketDisconnect:
            print(f"Client {client_id} disconnected")
            del connected_clients[client_id]
    else:
        print(f"Connection attempt failed for client {client_id}: Invalid token")
        await websocket.close(code=4001)


def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    start_server()