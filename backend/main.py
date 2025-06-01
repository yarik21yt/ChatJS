from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel
import json


app = FastAPI()
# CORS configuration
app.add_middleware( CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.messages: List[dict] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Client {client_id} connected successfully!")
        for message in self.messages:
            await websocket.send_json(message)
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        print(client_id)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    

    async def broadcast(self, message: dict):
        self.messages.append(message)
        if len(self.messages) > 10:
            self.messages.pop(0)
        print(self.active_connections.items())
        
        disconnected_clients = []
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except:
                disconnected_clients.append(client_id)
        
        for client_id in disconnected_clients:
            self.disconnect(client_id)



manager = ConnectionManager()


class MessageModel(BaseModel):
    client_id:str
    message:str

@app.post("/send")
async def send_message(message: MessageModel):
    await manager.broadcast({
        "type": "message",
        "client_id": message.client_id,
        "message": message.message,
        "timestamp": datetime.now().isoformat()
    })
    return True

@app.get("/messages")
async def get_messages():
    return {
        "messages": manager.messages
    }

@app.get("/connections")
async def get_connections():
    return {
        "active_connections": list(manager.active_connections.keys())
    }

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    await manager.broadcast({
        "type": "connection",
        "client_id": client_id,
        "message": f"Client {client_id} joined!",
        "timestamp": datetime.now().isoformat()
    })

    try:
        while True:
            data = await websocket.receive_json()
            #message_data = json.loads(data)
            await manager.broadcast({
                "type": "message",
                "client_id": client_id,
                "message": data.get("message", ""),
                "timestamp": datetime.now().isoformat()
            })
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast({
            "type": "disconnection",
            "client_id": client_id,
            "message": f"Client {client_id} left!",
            "timestamp": datetime.now().isoformat()
        })