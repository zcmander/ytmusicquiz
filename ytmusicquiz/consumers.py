import json

from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_name = 'game-{}'.format(self.game_id)
        print("Consumer", self.game_name)

        await self.channel_layer.group_add(
            "game",
            self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "game",
            self.channel_name)

    async def receive(self, text_data):
        print("REVEICE", text_data)

    async def game_status(self, event):
        print("EVENT", event)
        await self.send(json.dumps(event))