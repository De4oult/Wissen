from enum import Enum

from wissen_api import Wissen 

import functools
import traceback

class Handler(Enum):
    @staticmethod
    def spy(func = None, *, api_instance = Wissen) -> ...:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            
            except Exception as error:
                await Wissen.send_exception(''.join(traceback.format_exception(error)))

        return wrapper
    


# @Handler.spy
# async def test():  
#     return 1 / 0

# async def main():
#     Wissen.initialize('36297319:7b4e179fd6ae700c5b62014c250aa5cda60f29831f8a19d6af88a46909e102ef')

#     await test()

# import asyncio

# if __name__ == '__main__':
#     asyncio.run(main())