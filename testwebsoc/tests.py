import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/notification/broadcast/"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        
        # Send a message
        await websocket.send("Hello, WebSocket!")
        print("Message sent")

        # Receive a message
        response = await websocket.recv()
        print(f"Message received: {response}")

# Run the WebSocket test
asyncio.run(test_websocket())
