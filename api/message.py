from datetime import datetime

from emoji import emojize

class Message:
    def __init__(self, type: str, title: str = '', body: str = '') -> None:
        self.content: str = ''

        match type.lower():
            case 'info':     self.content += emojize(':closed_mailbox_with_raised_flag:  <b>ИНФОРМАЦИЯ</b> :closed_mailbox_with_raised_flag:', variant = 'emoji_type')
            case 'success':  self.content += emojize(':check_mark_button:  <b>УСПЕХ</b> :check_mark_button:', variant = 'emoji_type')
            case 'warning':  self.content += emojize(':warning:  <b>ПРЕДУПРЕЖДЕНИЕ</b> :warning:', variant = 'emoji_type')
            case 'error':    self.content += emojize(':no_entry:  <b>ОШИБКА</b> :no_entry:', variant = 'emoji_type')
            case 'critical': self.content += emojize(':fire:  <b>КРИТИЧЕСКАЯ ОШИБКА</b> :fire:', variant = 'emoji_type')
            case _:          return

        if title:
            self.content += '\n\n'
            self.content += f'<b>{title}</b>'
        
        if body:
            self.content += '\n\n'
            self.content += body

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return self.content

    async def store(self) -> None:
        ...