from supabase import create_client, Client

import os


class Supabase:
    def __init__(self) -> None:
        self.url: str = os.environ.get('SUPABASE_ENDPOINT')
        self.key: str = os.environ.get('SUPABASE_KEY')

        self.client: Client = create_client(self.url, self.key)

    async def push(self, table: str, query: str) -> None:
        self.client.table(table).insert(query).execute()

    async def get(self, table: str, query: str) -> list:
        return self.client.table(table).select(query).execute().data
    
    async def search(self, table: str, key_value: dict[str, any], requested_data: str) -> list:
        key:   str = list(key_value.keys())[0]
        value: any = key_value.get(key)

        return self.client.table(table).select(requested_data).eq(key, value).execute().data
    
    async def update(self, table: str, id: int, query: dict) -> None:
        self.client.table(table).update(query).eq('id', id).execute()

    
supabase_client: Supabase = Supabase()