# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        usuario = self.scope["user"]

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("entrou")
        text_data_json = json.loads(text_data)


        # Send message to room group
        usuario = str(self.scope["user"])
        message = usuario + ":" + text_data_json['message']



        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'usuario': usuario
            }

        )

    # Receive message from room group
    def chat_message(self, event):
        print(event)
        usuario = event["usuario"]
        print(usuario)
        message =  event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user':str(usuario)
        }))