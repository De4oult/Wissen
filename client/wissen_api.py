import requests
import json

ENDPOINT: str = 'http://localhost'

class API:
    def __init__(self) -> None:
        self.api_key: str = ''

    def initialize(self, api_key: str) -> None:
        self.api_key = api_key

        response_status: int = requests.get(
            f'{ENDPOINT}/authorize', 
            headers = {
                'Authorization' : self.api_key
            }
        ).status_code

        if response_status != 200:
            print('!!! Wissen key is invalid. Handling is not allowed')

    async def send_notification(self, type: str, title: str, body: str, language: str) -> None:
        if not self.api_key: return

        requests.post(
            f'{ENDPOINT}/notify',
            json = {
                'type'  : type,
                'title' : title,
                'body'  : body,
                'language' : language
            },
            headers = {
                'Authorization' : self.api_key,
                'Content-Type'  : 'application/json' 
            }
        )

    async def send_exception(self, body: str) -> None:
        if not self.api_key: return

        requests.post(
            f'{ENDPOINT}/notify',
            json = {
                'type'  : 'critical',
                'title' : 'Необработанное исключение',
                'body'  : body,
                'language' : 'python'
            },
            headers = {
                'Authorization' : self.api_key,
                'Content-Type'  : 'application/json' 
            }
        )

    # Counters
    def connect_counter(self, name: str, description: str = '', value: int = 0) -> int:
        if not self.api_key: return

        response = requests.post(
            f'{ENDPOINT}/authorize_counter',
            json = {
                'name'        : name,
                'description' : description,
                'value'       : value
            },
            headers = {
                'Authorization' : self.api_key,
                'Content-Type'  : 'application/json' 
            }
        )

        if response.status_code in [200, 201]:
            return response.json().get('id')


    async def get_counter(self) -> None:
        if not self.api_key: return

    async def update_counter(self) -> None:
        if not self.api_key: return


Wissen: API = API()