from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest

from message import Message
from database import supabase_client

import asyncio
import os


class Notifier:
    def __init__(self, api_key: str = None, channel_id: int = None) -> None:
        if (not api_key) and (not channel_id): return
        
        self.channel: int = channel_id
        self.api_key: str = api_key

        self.bot: Bot = Bot(token = os.environ.get('BOT_TOKEN'))

    async def init(self) -> None:
        self.channel = (await supabase_client.search('clients', { 'unique_key' : self.api_key }, 'channel_id'))[0].get('channel_id') if self.api_key else self.channel

    async def notify(self, message: Message) -> bool:
        try:
            await self.bot.send_message(
                chat_id    = self.channel, 
                text       = str(message),
                parse_mode = ParseMode.HTML
            )

            return True
            
        except TelegramBadRequest:
            return False