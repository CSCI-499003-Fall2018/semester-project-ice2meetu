from creation.models import Group
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if not self.user:
            await self.close()

        group = await self.get_group(user)
        self.group_id = str(group.pk) if group else None

        if not self.group_id:
            await self.close()

        # Join group
        await self.channel_layer.group_add(
            self.group_id,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_group(self, user):
        if user.eventuser_set.exists():
            eventuser = user.eventuser_set.all()[0]
            if not eventuser.is_playing():
                return None
            group = eventuser.current_group()
            return group if group else None
        return None


    async def disconnect(self, close_code):
        if not self.group_id:
            await self.close()
        # Leave group connection
        await self.channel_layer.group_discard(
            self.group_id,
            self.channel_name
        )
    
    @database_sync_to_async
    def set_group_complete(self):
        group = Group.objects.get(pk=int(self.group_id))
        if not group.is_complete:
            group.is_complete = True
            group.save()

    # Receive message from WebSocket
    async def receive(self, text_data):
        if not self.group_id:
            await self.close()
            
        text_data_json = json.loads(text_data)
        complete = text_data_json['complete']

        if complete:
            await self.set_group_complete()

        # Notify group
        await self.channel_layer.group_send(
            self.group_id,
            {
                'type': 'notify',
                'complete': True
            }
        )

    # Receive message from group
    async def notify(self, event):
        if not self.group_id:
            await self.close()
            
        complete = event['complete']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'complete': True
        }))
