from wissen_api import Wissen


class Counter:
    def __init__(self, name: str, description: str = '', value: int = 0) -> None:
        self.name: str = name
        self.description: str = description
        self.value: int = value
        
        self.id = Wissen.connect_counter(self.name, self.description, self.value)

        self.__get_counter()

    def __update_counter(self) -> None:
        Wissen.update_counter(self.id, self.value)

    def __get_counter(self) -> None:
        counter = Wissen.get_counter(self.id)

        if not counter: return

        self.name = counter.get('name')
        self.description = counter.get('description')
        self.value = counter.get('value')

    def get(self) -> int:
        return self.value

    def set(self, other: int) -> None:
        self.value = other
        self.__update_counter()

    def increment(self) -> None:
        self.value += 1
        self.__update_counter()

    def decrement(self) -> None:
        self.value -= 1
        self.__update_counter()

    def __add__(self, other: int) -> None:
        if not isinstance(other, int): raise TypeError('unsupported operand for +: ', f'\'{type(self).__name__}\' and \'{type(other).__name__}\'')

        self.value += other
        self.__update_counter()
        
        return self        
    
    def __sub__(self, other: int) -> None:
        if not isinstance(other, int): raise TypeError('unsupported operand for -: ', f'\'{type(self).__name__}\' and \'{type(other).__name__}\'')

        self.value -= other
        self.__update_counter()
        
        return self

    def __str__(self) -> str:
        return f'{self.id}_{self.name}: {self.value}'



# Wissen.initialize('36297319:7b4e179fd6ae700c5b62014c250aa5cda60f29831f8a19d6af88a46909e102ef')

# test = Counter('testCounter')

# test.increment()
# test += 10

# print(test)

# test -= 5

# print(test)