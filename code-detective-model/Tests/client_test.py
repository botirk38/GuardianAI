import asyncio
import websockets

async def connect_to_server():
    uri = "ws://localhost:8000/ws/test_client?token=1090"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        await websocket.send("Hello Server!")
        response = await websocket.recv()
        print(f"Received from server: {response}")

if __name__ == "__main__":
    asyncio.run(connect_to_server())
