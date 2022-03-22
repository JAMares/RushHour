from asyncio.windows_events import NULL



class Node:
    father= NULL
    movements= 0
    blocked= 0
    state= []

    def __init__(self):
        pass
        

    def __init__(self, father, movements, blocked, estado):
        self.father = father
        self.movements = movements
        self.blocked = blocked
        self.state = estado

    def get_Fn(self):
        return self.blocked + self.movements

class Graph:

    def __init__(self) -> None:
        pass

    def __init__(self, inicio):
        self.inicio = inicio
