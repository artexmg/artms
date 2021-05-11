from channels.generic.websocket import AsyncWebsocketConsumer
import json
# Main consumer structure learned from
# this tutorial https://www.youtube.com/watch?v=32iJlPDNLQY&t=926s
# NOTE: while the code is broken the content is great

class DashConsumer(AsyncWebsocketConsumer):
    """
    Main consumer class
    """
    async def connect(self):
        """
        asynchronous connection
        """
        self.groupname = 'dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        just
        """
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        receive data from my websocket connection!
        """
        datapoint = json.loads(text_data)
        val = datapoint['value']

        await self.channel_layer.group_send(
            self.groupname,
            {
                'type': 'deprocessing',
                'value': val
            }
        )
        # print (text_data)


    async def deprocessing(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({'value': valOther}))
