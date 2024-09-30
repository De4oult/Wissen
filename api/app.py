from sanic import Sanic
from sanic.response import HTTPResponse, json, html
from sanic.request import Request
from sanic_cors import CORS
from hashlib import sha256
from random import randint

from notifier import Notifier
from message import Message
from database import supabase_client

from dotenv import load_dotenv

load_dotenv()

app = Sanic("telegram_bot")

CORS(app)


@app.route('/register', methods = ['POST'])
async def register_post(request: Request) -> HTTPResponse:
    if not all(key in request.json for key in ['name', 'channel_id']): return json({ 'message' : 'Need name and channel_id' }, status = 400)
    if len(await supabase_client.search('clients', { 'channel_id' : request.json.get('channel_id') }, '*')): return json({ 'message' : 'Channel already registered' }, status = 400)

    name: str       = str(request.json.get('name'))
    channel_id: int = int(request.json.get('channel_id'))

    notifier: Notifier = Notifier(channel_id = channel_id)

    response: bool = await notifier.notify(Message('info', 'Приложение зарегистрировано в Wissen'))

    if not response: 
        return json({ 'message' : 'Not valid channel_id' }, status = 400)

    initial_int: int = randint(10000000, 99999999)

    api_key: str    = '%d:%s' % (initial_int, str(sha256(f'{name}_{channel_id}'.encode('utf-8')).hexdigest()))
    history_id: str = '%d_%s' % (initial_int, str(sha256(f'{name}'.encode('utf-8')).hexdigest())[:12])

    await supabase_client.push('clients', {
        'name'       : name,
        'channel_id' : channel_id,
        'unique_key' : api_key,
        'history_id' : history_id
    })

    await notifier.notify(Message('info', f'Ваша ссылка для просмотра истории: <code>{history_id}</code>'))

    return json({ 
        'message' : 'Successfully registered', 
        'api_key' : api_key,
        'history_id' : history_id
    }, status = 201)

@app.route('/notify', methods = ['POST'])
async def notify_post(request: Request) -> HTTPResponse:
    if not request.headers.get('Authorization'): return json({ 'message' : 'Specify a api_key for sending messages' }, status = 400)
    if not request.json.get('type'):    return json({ 'message' : 'Specify a type of the message' }, status = 400)
    if (not request.json.get('title')) and (not request.json.get('body')):
        return json({ 'message' : 'Specify a title or a body of the message' }, status = 400)

    message: Message = Message(
        request.json.get('type'),
        request.json.get('title'),
        request.json.get('body')
    )
    
    notifier: Notifier = Notifier(request.headers.get('Authorization'))
    await notifier.init()
    
    await notifier.notify(message)

    return json({ 'message' : 'Successfully processed' }, status = 200)

@app.route('/history', methods = ['GET'])
async def history_get(request: Request) -> HTTPResponse:
    print(request.args.get('history_id'))

    return html() # return histroy mit alpine

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0', 
        port = 8000
    )
