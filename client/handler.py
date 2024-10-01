from enum import Enum

from wissen_api import Wissen 

import functools
import traceback
import inspect

class Handler(Enum):
    @staticmethod
    def spy(func = None, *, api_instance = Wissen) -> ...:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)

                except Exception as error:
                    await Wissen.send_exception(''.join(traceback.format_exception(error)))

                    raise error

        return wrapper
    
    @staticmethod
    def silent(func = None, *, api_instance = Wissen) -> ...:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            
            except Exception as error:
                await Wissen.send_exception(''.join(traceback.format_exception(error)))

                print('Wissen has stopped program')

        return wrapper

    @staticmethod
    def observe(func = None, *, api_instance = Wissen) -> ...:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)                

                frame = inspect.currentframe().f_back

                # Перехватываем локальные переменные после завершения функции
                locals_variables = frame.f_locals

                print(locals_variables)

                return result

            except Exception as error:
                await Wissen.send_exception(''.join(traceback.format_exception(error)))

                print('Wissen has stopped program')

        return wrapper


# @Handler.observe
# async def test():
#     a = 10

#     b = a * 2

#     c = b / a

#     print(c)

#     return 10

# async def main():
#     # Wissen.initialize('36297319:7b4e179fd6ae700c5b62014c250aa5cda60f29831f8a19d6af88a46909e102ef')

#     print(await test())

# import asyncio

# if __name__ == '__main__':
#     asyncio.run(main())