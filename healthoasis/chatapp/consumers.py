from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.username = self.scope['user'].username

        # Send message to room group when user connects
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "system_message",
                "message": f"'{self.username}' connected",
                "timestamp": str(datetime.datetime.now().strftime("%H:%M:%S"))
            }
        )

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Send message to room group when user disconnects
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "system_message",
                "message": f"'{self.username}' disconnected",
                "timestamp": str(datetime.datetime.now().strftime("%H:%M:%S"))
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                'username': self.username,
                'is_staff': self.scope['user'].is_staff,
                'timestamp': str(datetime.datetime.now().strftime("%H:%M:%S"))
            }
        )

    # Receive system message from room group
    def system_message(self, event):
        message = f"System: ({event['timestamp']}) {event['message']}"
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    # Receive chat message from room group
    def chat_message(self, event):
        username = event['username']
        is_staff = event['is_staff']
        pre = "'" + username
        if(is_staff == 1):
            pre += "' (STAFF)"
        else:
            pre += "'"

        message = f"{event['timestamp']} | {pre}:\n\t- {event['message']}\n"
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
