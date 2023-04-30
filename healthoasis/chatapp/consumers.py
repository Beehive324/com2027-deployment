import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

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
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                'username': self.scope['user'].username,
                'is_staff': self.scope['user'].is_staff,
                'timestamp': str(datetime.datetime.now().strftime("%H:%M:%S"))
            }
        )


    # Receive message from room group
    def chat_message(self, event):
        username = event['username']
        is_staff = event['is_staff']
        pre = username
        if(is_staff == 1):
            pre += " (STAFF)"
            
        message = "From '" + pre + "': " + event["message"] + "\n(" + event['timestamp'] + ")\n"
        # Send message to WebSocket
       
        self.send(text_data=json.dumps({"message": message}))