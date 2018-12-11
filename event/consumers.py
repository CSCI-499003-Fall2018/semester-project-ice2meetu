from creation.models import Group
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json   


class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("EVENT CONSUMER")
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        
        self.event_codes = await self.get_access_codes(user)

        if not self.event_codes:
            await self.close()

        # Join group
        for code in self.event_codes:
            await self.channel_layer.group_add(
                code,
                self.channel_name
            )

        await self.accept()

    @database_sync_to_async
    def get_access_codes(self, user):
        if user.eventuser_set.exists():
            eventuser = user.eventuser_set.all()[0]
            codes = [event.access_code for event in eventuser.events.all()]
            return codes
        else:
            return None
    
    async def disconnect(self, close_code):
        if not self.event_codes:
            await self.close()

        # Leave group connection
        for code in self.event_codes:
            await self.channel_layer.group_discard(
                code,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        if not self.event_codes:
            await self.close()

        text_data_json = json.loads(text_data)
        event_code = text_data_json['event_code']
        event_title = text_data_json['event_title']
        notification = text_data_json['notification']

        # Send message to group
        await self.channel_layer.group_send(
            event_code,
            {
                'type': 'notify',
                'event_code': event_code,
                'event_title': event_title,
                'notification': notification
            }
        )

    # Receive message from group
    async def notify(self, event):
        if not self.event_codes:
            await self.close()

        notification = event['notification']
        event_code = event['event_code']
        event_title = event['event_title']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'event_code': event_code,
            'event_title': event_title,
            'notification': notification
        }))

