import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_group_name = "pong_game"

		await self.channel_layer.group_add()(self.room_group_name, self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_dicard(self.room_group_name, self.channel_name)
