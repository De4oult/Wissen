from sanic import Sanic
from sanic.response import HTTPResponse, json, html
from sanic.exceptions import NotFound, MethodNotAllowed
from sanic.request import Request
from sanic_cors import CORS
from hashlib import sha256
from random import randint

from notifier import Notifier
from message import Message
from database import supabase_client
from frontend import frontend

import os

app = Sanic('Wissen')

CORS(app)


@app.route('/authorize', methods = ['GET'])
async def authorize_get(request: Request) -> HTTPResponse:
    if not request.headers.get('Authorization'): return json({ 'message' : 'Specify a api key for authorize' }, status = 400)

    client_exist: int = len(await supabase_client.search('clients', { 'unique_key' : request.headers.get('Authorization') }, 'id'))

    if not client_exist: return json({ 'message' : 'Invalid api key' }, status = 401)

    return json({ 'message' : 'Successfully authorized' }, status = 200)

@app.route('/register', methods = ['POST'])
async def register_post(request: Request) -> HTTPResponse:
    if not all(key in request.json for key in ['name', 'channel_id']): return json({ 'message' : 'Need name and channel_id' }, status = 400)
    if len(await supabase_client.search('clients', { 'channel_id' : request.json.get('channel_id') }, '*')): return json({ 'message' : 'Channel already registered' }, status = 400)

    name: str       = str(request.json.get('name'))
    channel_id: int = int(request.json.get('channel_id'))

    notifier: Notifier = Notifier(channel_id = channel_id)

    response = await notifier.notify(Message('info', 'Приложение зарегистрировано в Wissen'))

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

    message = await notifier.notify(Message('info', f'Ваша ссылка для просмотра истории: <a href="https://wissen.onrender.com/history?id={history_id}">https://wissen.onrender.com/history?id={history_id}</a>'))

    await notifier.pin(message.message_id)

    return json({ 
        'message' : 'Successfully registered', 
        'api_key' : api_key,
        'history_id' : history_id
    }, status = 201)

@app.route('/notify', methods = ['POST'])
async def notify_post(request: Request) -> HTTPResponse:
    if not request.headers.get('Authorization'): return json({ 'message' : 'Specify a api key for sending messages' }, status = 400)
    if not request.json.get('type'): return json({ 'message' : 'Specify a type of the message' }, status = 400)
    if (not request.json.get('title')) and (not request.json.get('body')):
        return json({ 'message' : 'Specify a title or a body of the message' }, status = 400)

    message: Message = Message(
        request.json.get('type'),
        request.json.get('title'),
        request.json.get('body'),
        request.json.get('language')
    )
    
    notifier: Notifier = Notifier(request.headers.get('Authorization'))
    await notifier.init()
    
    await notifier.notify(message)

    return json({ 'message' : 'Successfully processed' }, status = 200)

@app.route('/authorize_counter', methods = ['POST'])
async def authorize_counter_post(request: Request) -> HTTPResponse:
    if not request.headers.get('Authorization'): return json({ 'message' : 'Specify a api key for authorize counter' }, status = 400)
    if not request.json.get('name'): return json({ 'message' : 'Specify a name of the counter' }, status = 400)

    response: list = await supabase_client.search('clients', { 'unique_key' : request.headers.get('Authorization') }, 'id')

    if not len(response): return json('Invalid api key', status = 401)

    user_id: int = response[0].get('id')

    counter: list = await supabase_client.search('counters', { 'name' : request.json.get('name'), 'user_id' : user_id }, 'id')
    
    if len(counter):
        return json({ 'message': 'Counter already exists', 'id' : counter[0].get('id') }, status = 200)

    await supabase_client.push('counters', {
        'name'        : request.json.get('name'),
        'description' : request.json.get('description', ''),
        'value'       : request.json.get('value', 0),
        'user_id'     : user_id
    })

    new_counter = (await supabase_client.search('counters', { 'name' : request.json.get('name'), 'user_id' : user_id }, 'id'))[0]
    
    return json({ 'message' : 'Counter successfully registered', 'id' : new_counter.get('id') }, status = 201)

@app.route('/get_counter', methods = ['GET'])
async def get_counter_get(request: Request) -> HTTPResponse:
    if not request.headers.get('Authorization'): return json({ 'message' : 'Specify a api key for authorize counter' }, status = 400)
    if not request.args.get('id'): return json({ 'message' : 'Specify an id of the counter' }, status = 400)

    response: list = await supabase_client.search('clients', { 'unique_key' : request.headers.get('Authorization') }, 'id')

    if not len(response): return json({ 'message' : 'Invalid api key' }, status = 401)

    counter = await supabase_client.search('counters', { 'id' : request.args.get('id') }, '*')

    if not len(counter):
        return json({ 'message': 'Counter not exists', 'id' : request.args.get('id') }, status = 400)
    
    return json({ 'message' : 'Counter successfully gotten', 'counter' : counter[0] }, status = 200)

@app.route('/update_counter', methods = ['GET'])
async def update_counter_get(request: Request) -> HTTPResponse:
    if not request.headers.get('Authorization'): return json({ 'message' : 'Specify a api key for authorize counter' }, status = 400)
    if (not request.args.get('id')) or (not request.args.get('value')): return json({ 'message' : 'Specify an id and a value of the counter' }, status = 400)

    response: list = await supabase_client.search('clients', { 'unique_key' : request.headers.get('Authorization') }, 'id')

    if not len(response): return json({ 'message' : 'Invalid api key' }, status = 401)

    counter = await supabase_client.search('counters', { 'id' : request.args.get('id') }, '*')

    if not len(counter):
        return json({ 'message': 'Counter not exists', 'id' : request.args.get('id') }, status = 400)
    
    await supabase_client.update('counters', request.args.get('id'), {
        'value' : request.args.get('value')
    })

    return json({ 'message' : 'Counter successfully updated' }, status = 200)

# Pages
@app.route('/history', methods = ['GET'])
async def history_get(request: Request) -> HTTPResponse:
    if not request.args.get('id'): return html(frontend.page('error', { 'error_message' : 'Не указан идентификатор истории' }), status = 400)

    response: list = await supabase_client.search('clients', { 'history_id' : request.args.get('id') }, 'name')
    
    if not len(response): return html(frontend.page('error', { 'error_message' : 'Недействительная ссылка на историю' }), status = 400)

    history_data: list[dict] = await supabase_client.search('messages', { 'history_id' : request.args.get('id') }, '*')
    
    return html(frontend.page('history', { 'name' : response[0].get('name'), 'history_data' : sorted(history_data, key = lambda record: record.get('id'), reverse = True) }), status = 200)

@app.route('/record/<record_id:int>', methods = ['GET'])
async def record_id_get(request: Request, record_id: int) -> HTTPResponse:
    response: list = await supabase_client.search('messages', { 'id' : record_id }, '*')

    if not len(response): return html(frontend.page('error', { 'error_message' : f'Не удалось найти сообщение с id == {record_id}' }), status = 400)

    return html(frontend.page('record', { 'record_data' : response[0] }), status = 200)

# Errors
@app.exception(NotFound)
async def not_found_exception(request: Request, exception: Exception) -> HTTPResponse:
    return html(frontend.page('error', { 'error_message' : '404. Кажется, тут ничего нет...' })) 

@app.exception(Exception)
async def server_error_exception(request: Request, exception: Exception) -> HTTPResponse:
    return html(frontend.page('error', { 'error_message' : '500. Серверу сейчас нехорошо 🤒' })) 

@app.exception(MethodNotAllowed)
async def method_not_allowed_exception(request: Request, exception: Exception) -> HTTPResponse:
    return html(frontend.page('error', { 'error_message' : '405. Так делать нельзя 🚧' }))

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0', 
        port = int(os.environ.get('PORT', 80))
    )
