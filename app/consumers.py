from channels.generic.websocket import AsyncWebsocketConsumer
from collections import deque

connected_clients = {}


class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get subdomain from URL
        self.subdomain = self.scope['url_route']['kwargs']['subdomain']
        print(f"Connecting subdomain: {self.subdomain}")

        # Accept the WebSocket connection
        await self.accept()

        # Check if the subdomain already has an active connection
        if self.subdomain in connected_clients:
            await self.send({"status": "app_exists"})
            await self.close()
            return

        # Create a new queue for this connection
        self.queue = deque()
        connected_clients[self.subdomain] = (self, self.queue)
        print(f"Connected clients: {connected_clients}")

    async def disconnect(self, close_code):
        # Remove client from connected_clients on disconnect
        print(f"Client {self.subdomain} disconnected")
        connected_clients.pop(self.subdomain, None)

    async def receive(self, text_data):
        # Handle messages received from the client
        print(f"Received from {self.subdomain}: {text_data}")
        self.queue.append(text_data)
