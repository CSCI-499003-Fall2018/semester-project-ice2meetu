from creation.models import Group
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer
import json


class GroupConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        eventuser = user.eventuser_set.all()[0]
        group = eventuser.current_group()
        self.group_id = str(group.pk)

        # Join group
        async_to_sync(self.channel_layer.group_add)(
            self.group_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave group connection
        async_to_sync(self.channel_layer.group_discard)(
            self.group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        complete = text_data_json['complete']

        if complete:
            group = Group.objects.get(pk=self.group_id)
            if not group.is_complete:
                group.is_complete = True
                group.save()

        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.group_id,
            {
                'type': 'notify',
                'complete': True
            }
        )

    # Receive message from group
    def notify(self, event):
        complete = event['complete']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'complete': True
        }))
