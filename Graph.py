from asyncio.windows_events import NULL
from syslog import closelog


class Nodo:
    father= NULL
    movimientos= 0
    bloqueos= 0
    estado= []

    def __init__(self, father, movimientos, bloqueos, estado):
        self.father = father
        self.movimientos = movimientos
        self.bloqueos = bloqueos
        self.estado = estado

    def get_Fn(self):
        return self.bloqueos + self.movimientos

class Graph:

    def __init__(self, inicio):
        self.inicio = inicio
