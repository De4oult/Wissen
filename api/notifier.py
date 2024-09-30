from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram import types

from message import Message
from database import supabase_client

import os


class Notifier:
    def __init__(self, api_key: str = None, channel_id: int = None) -> None:
        if (not api_key) and (not channel_id): return

        self.channel: int = channel_id
        self.api_key: str = api_key
        
        self.history_id: str | None = None

        self.bot: Bot = Bot(token = os.environ.get('BOT_TOKEN'))

    async def init(self) -> None:
        if not self.api_key: return

        response: dict[str, any] = (await supabase_client.search('clients', { 'unique_key' : self.api_key }, 'channel_id, history_id'))

        if not len(response): return

        response = response[0]

        self.channel    = response.get('channel_id')
        self.history_id = response.get('history_id')

    async def notify(self, message: Message) -> types.message.Message | bool:
        try:
            tg_message = await self.bot.send_message(
                chat_id    = self.channel, 
                text       = str(message),
                parse_mode = ParseMode.HTML
            )

            if self.history_id: await message.store(tg_message.message_id, self.history_id)

            return tg_message
            
        except TelegramBadRequest:
            return False
        
    async def pin(self, message_id: int) -> None:
        await self.bot.pin_chat_message(self.channel, message_id)