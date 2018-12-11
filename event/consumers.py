from creation.models import Group
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json   


class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
            
        self.event_code = await self.get_access_code(user)

        if not self.event_code:
            await self.close()

        # Join group
        await self.channel_layer.group_add(
            self.event_code,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_access_code(self, user):
        if user.eventuser_set.exists():
            eventuser = user.eventuser_set.all()[0]
            event = eventuser.playing_event()
            if not event:
                print("no playing event")
            return event.access_code if event else None
        else:
            return None
    
    async def disconnect(self, close_code):
        if not self.event_code:
            await self.close()

        # Leave group connection
        await self.channel_layer.group_discard(
            self.event_code,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        if not self.event_code:
            await self.close()

        text_data_json = json.loads(text_data)
        notification = text_data_json['notification']

        # Send message to group
        await self.channel_layer.group_send(
            self.event_code,
            {
                'type': 'notify',
                'notification': notification
            }
        )

    # Receive message from group
    async def notify(self, event):
        if not self.event_code:
            await self.close()

        notification = event['notification']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification': notification
        }))

