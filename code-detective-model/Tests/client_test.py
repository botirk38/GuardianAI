import asyncio
import websockets

async def connect_to_server():
    uri = "ws://localhost:8001/ws/test_client?token=1090"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        try:
            while True:
                message = await websocket.recv()
                print(f"Received from server: {message}")
        except websockets.ConnectionClosed:
            print("Server connection was closed")

if __name__ == "__main__":
    asyncio.run(connect_to_server())
