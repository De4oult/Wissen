from wissen_api import Wissen


class Counter:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.description: str = ''
        self.value: int = 0
        
        self.id = Wissen.connect_counter(self.name, self.description, self.value)

    def __update_counter(self) -> None:
        ...

    def get(self) -> int:
        return self.value

    def set(self, other: int) -> None:
        self.value = other

    def increment(self) -> None:
        self.value += 1

    def decrement(self) -> None:
        self.value -= 1

    def __add__(self, other: int) -> None:
        if not isinstance(other, int): raise TypeError('unsupported operand for +: ', f'\'{type(self).__name__}\' and \'{type(other).__name__}\'')

        self.value += other
        
        return self
        
    
    def __sub__(self, other: int) -> None:
        if not isinstance(other, int): raise TypeError('unsupported operand for -: ', f'\'{type(self).__name__}\' and \'{type(other).__name__}\'')

        self.value -= other
        
        return self

    def __str__(self) -> str:
        return f'{self.counter_id}_{self.name}: {self.value}'
    

test = Counter()

test.create('testCounter', value = 1)

test.increment()

test += 10

print(test)

test -= 5

print(test)