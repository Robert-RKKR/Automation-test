# Django Import:
from channels.generic.websocket import AsyncWebsocketConsumer


class CollectConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.channel_layer.group_add('collect', self.channel_name)
        await self.accept()

    """async def disconnect(self):
        await self.channel_layer.group_discard('collect', self.channel_name)"""

    async def send_collect(self, event):
        text_message = event['text']
        await self.send(text_message)
