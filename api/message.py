from emoji import emojize

from database import supabase_client

class Message:
    def __init__(self, type: str, title: str = '', body: str = '') -> None:
        self.content: str = ''

        self.type: str  = type
        self.title: str = title
        self.body: str  = body

        match self.type.lower():
            case 'info':     self.content += emojize(':closed_mailbox_with_raised_flag:  <b>ИНФОРМАЦИЯ</b> :closed_mailbox_with_raised_flag:', variant = 'emoji_type')
            case 'success':  self.content += emojize(':check_mark_button:  <b>УСПЕХ</b> :check_mark_button:', variant = 'emoji_type')
            case 'warning':  self.content += emojize(':warning:  <b>ПРЕДУПРЕЖДЕНИЕ</b> :warning:', variant = 'emoji_type')
            case 'error':    self.content += emojize(':no_entry:  <b>ОШИБКА</b> :no_entry:', variant = 'emoji_type')
            case 'critical': self.content += emojize(':fire:  <b>КРИТИЧЕСКАЯ ОШИБКА</b> :fire:', variant = 'emoji_type')
            case _:          return

        if title:
            self.content += '\n\n'
            self.content += f'<b>{self.title}</b>'
        
        if body:
            self.content += '\n\n'
            self.content += self.body

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return self.content

    async def store(self, message_id: int, history_id: str) -> None:
        await supabase_client.push('messages', {
            'type' : self.type,
            'title' : self.title,
            'body' : self.body,

            'tg_message_id' : message_id,
            'history_id' : history_id
        })