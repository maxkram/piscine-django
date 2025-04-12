import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if self.room_group_name not in self.connected_users:
            self.connected_users[self.room_group_name] = set()
        self.connected_users[self.room_group_name].add(self.user.username)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send last 3 messages with timestamps
        last_messages = await self.get_last_messages()
        for msg in last_messages:
            await self.send(text_data=json.dumps({
                'message': msg['message'],  # Use pre-formatted message
                'timestamp': msg['timestamp'],
                'full_timestamp': msg['full_timestamp']
            }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{self.user.username} has joined the chat",
                'timestamp': self.now_timestamp(),
                'full_timestamp': self.now_full_timestamp()
            }
        )
        await self.update_user_list()

    async def disconnect(self, close_code):
        self.connected_users[self.room_group_name].discard(self.user.username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{self.user.username} has left the chat",
                'timestamp': self.now_timestamp(),
                'full_timestamp': self.now_full_timestamp()
            }
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.update_user_list()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{self.user.username}: {message}",
                'timestamp': self.now_timestamp(),
                'full_timestamp': self.now_full_timestamp()
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'timestamp': event['timestamp'],
            'full_timestamp': event['full_timestamp']
        }))

    async def user_list(self, event):
        await self.send(text_data=json.dumps({
            'users': event['users']
        }))

    @database_sync_to_async
    def save_message(self, content):
        room = ChatRoom.objects.get(name=self.room_name)
        Message.objects.create(room=room, user=self.user, content=content)

    async def update_user_list(self):
        users = list(self.connected_users[self.room_group_name])
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': users
            }
        )

    @database_sync_to_async
    def get_last_messages(self):
        room = ChatRoom.objects.get(name=self.room_name)
        messages = Message.objects.filter(room=room).select_related('user').order_by('-timestamp')[:3][::-1]
        return [{
            'message': f"{msg.user.username}: {msg.content}",
            'timestamp': msg.timestamp.strftime('%H:%M:%S'),
            'full_timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]

    def now_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%H:%M:%S')

    def now_full_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')