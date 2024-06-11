import asyncio
from consumer import consume
from websocket_server import start_websocket_server


async def main():
    # Start the WebSocket server
    websocket_task = asyncio.create_task(start_websocket_server())

    # Start the Kafka consumer
    consumer_task = asyncio.create_task(consume())

    await asyncio.gather(websocket_task, consumer_task)

if __name__ == "__main__":
    # Run the main function with asyncio
    asyncio.run(main())

