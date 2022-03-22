from asyncio.windows_events import NULL
from time import time
from Graph import *
from RushHour import *


# SCREEN DATA
_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': 0, 'lineWidth': 2}

def algorithm_AStar(start_node):

    end_node = NULL

    return 0


def main():

    init_node = Node(NULL, 0, 0, [])

    graph = Graph(init_node)

    open_nodes = []

    close_nodes = []

    drawing = True

    createBoard(drawing)



if __name__ == '__main__':
    main()
