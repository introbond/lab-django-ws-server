# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class MyConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        location = text_data_json["location"]
        max_room = text_data_json["max_room"]
        avaliable_room = text_data_json["avaliable_room"]
        trigger_count = text_data_json["trigger_count"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {"type": "chat_message", 
                "location": location,
                "max_room":max_room,
                "avaliable_room":avaliable_room,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {
                "location": event["location"],
                "max_room": event["max_room"],
                "avaliable_room": event["avaliable_room"],
            }))