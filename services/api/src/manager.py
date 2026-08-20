from fastapi import WebSocket



class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        self.active_connections[user_id] = ws

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, user_id: str, message: str):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_text(message)

manager = ConnectionManager()
