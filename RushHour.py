from asyncio.windows_events import NULL
from pickle import REDUCE
import sys
import pygame
from pygame.locals import KEYDOWN, K_q, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_1, K_9
from Board import *
from Graph import *

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (160, 160, 160)


GAMEBOARD = NULL

# SCREEN DATA
_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': 0, 'lineWidth': 2}
# CURRENT SELECTED VEHICLE
global CURR_VEHICLE
# INITIALIZES GAME BOARD, WIN POS AT x:6, y:2 (OUTSIDE MAIN PLAY AREA)


def createNodes(node: Node, board: Board, openNodes, closeNodes):
    movementCount = node.movements+1
    possibleStates = board.expandPossibleStates()

    # THIS ALREADY CHECKS IF EACH NODE STATE DOESN'T EXIST ALREADY
    for state in possibleStates:
        board.boardMAP = state
        hCost = board.calculateCurrentStateCost()
        newNode = Node(node, movementCount, hCost, state)

        if checkIfCloseNode(newNode, closeNodes):
            continue

        openNodes = setOpenNodes(newNode, openNodes)

    # SORTS NODES BASED ON COST
    openNodes = sorted(openNodes, key=lambda node: node.get_Fn())
    return openNodes

# Function to insert open nodes avoiding repetitions


def setOpenNodes(newNode, openNodes):
    state = newNode.state

    for openNode in openNodes:
        if (state == openNode.state).all():
            return openNodes  # Ignore the reapeated node

    # Depending on the intent, this could be changed to an ordered insert
    openNodes.append(newNode)
    return openNodes

# Function to check if a node was already considerate before


def checkIfCloseNode(newNode, closeNodes):
    state = newNode.state

    for closedNode in closeNodes:
        if (state == closedNode.state).all():
            return True

    return False


def a_estrella(root: Node, open_nodes, close_nodes, GAMEBOARD):
    currentNode = root
    
    while (currentNode.blocked > 0):
        currentNode = open_nodes.pop(0)
        print(len(close_nodes))
        close_nodes.append(currentNode)
        open_nodes = createNodes(
            currentNode, GAMEBOARD, open_nodes, close_nodes)
    solution = []
    while(currentNode != root):
        solution.append(currentNode)
        currentNode = currentNode.father
    solution.reverse()
    return solution


def main():
    global CURR_VEHICLE
    # NO SELECTED VEHICLE
    CURR_VEHICLE = -1
    # FILE PATH SELECTION SHOULD BE WITHIN INTERFACE
    GAMEBOARD = Board(6, (6, 2), "./problems.txt")
    GAMEBOARD.generatePuzzle()
    open_nodes = []
    close_nodes = []

    father_node = Node(
        NULL, 0, GAMEBOARD.calculateCurrentStateCost(), GAMEBOARD.boardMAP)
    close_nodes.append(father_node)
    open_nodes = createNodes(father_node, GAMEBOARD, open_nodes, close_nodes)
    print(a_estrella(father_node, open_nodes, close_nodes, GAMEBOARD))

    graph = Graph(father_node)

    pygame.init()

    _VARS['gridCells'] = GAMEBOARD.boardMAP.shape[0]

    pygame.display.set_caption('Rush Hour')
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    while True:
        checkEvents(GAMEBOARD, open_nodes)
        _VARS['surf'].fill(GREY)
        drawSquareGrid(
            _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
        placeCells(GAMEBOARD)
        pygame.display.update()
        # CHECKS FOR WIN STATE
        if(GAMEBOARD.hasWon() == True):
            print("GAME WON, NEXT LEVEL")
            return
            # GOES TO NEXT LEVEL
            # GAMEBOARD.generatePuzzle()


# NEW METHOD FOR ADDING CELLS :
def placeCells(BOARD):
    # GET CELL DIMENSIONS...
    cellBorder = 6
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    # DOUBLE LOOP
    for row in range(BOARD.boardMAP.shape[0]):
        for column in range(BOARD.boardMAP.shape[1]):
            # CHECKS IF VEHICLES ARE WITHIN A TILE
            if(BOARD.boardMAP[row][column] != 0):
                v = BOARD.getVehicle(BOARD.boardMAP[row][column])
                x = _VARS['gridOrigin'][0] + (celldimY*row) + cellBorder + \
                    (2*row*cellBorder) + _VARS['lineWidth']/2
                y = _VARS['gridOrigin'][1] + (celldimX*column) + cellBorder + (
                    2*column*cellBorder) + _VARS['lineWidth']/2
                drawSquareCell(x, y, celldimX, celldimY, v.color)

                # DRAWING CORRESPONDING ID FOR EACH VEHICLE CELL
                font = pygame.font.SysFont('arial', 15)
                vId = BOARD.boardMAP[row][column]
                # IF VEHICLE IS SELECTED, DRAW THE TEXT WHITE
                if(vId == CURR_VEHICLE):
                    text = font.render(
                        str(vId), True, WHITE)
                else:
                    text = font.render(
                        str(vId), True, BLACK)
                _VARS['surf'].blit(text, (x+cellBorder, y))
    # DRAW WIN TILE
    if(BOARD.hasWon() == False):
        drawSquareCell(
            _VARS['gridOrigin'][0] + (celldimY*BOARD.goalPos[0])
            + cellBorder + (2*BOARD.goalPos[0]
                            * cellBorder) + _VARS['lineWidth']/2,
            _VARS['gridOrigin'][1] + (celldimX*BOARD.goalPos[1])
            + cellBorder + (2*BOARD.goalPos[1]*cellBorder) +
            _VARS['lineWidth']/2,
            celldimX, celldimY, GREEN)


# Draw filled rectangle at coordinates


def drawSquareCell(x, y, dimX, dimY, color):
    pygame.draw.rect(
        _VARS['surf'], color,
        (x, y, dimX, dimY)
    )


def drawSquareGrid(origin, gridWH, cells):

    CONTAINER_WIDTH_HEIGHT = gridWH
    cont_x, cont_y = origin

    # DRAW Grid Border:
    # TOP lEFT TO RIGHT
    pygame.draw.line(
        _VARS['surf'], BLACK,
        (cont_x, cont_y),
        (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), _VARS['lineWidth'])
    # # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
        _VARS['surf'], BLACK,
        (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
        (CONTAINER_WIDTH_HEIGHT + cont_x,
            CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])
    # # LEFT TOP TO BOTTOM
    pygame.draw.line(
        _VARS['surf'], BLACK,
        (cont_x, cont_y),
        (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), _VARS['lineWidth'])
    # # RIGHT TOP TO BOTTOM
    pygame.draw.line(
        _VARS['surf'], BLACK,
        (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
        (CONTAINER_WIDTH_HEIGHT + cont_x,
            CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])

    # Get cell size, just one since its a square grid.
    cellSize = CONTAINER_WIDTH_HEIGHT/cells

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(cells):
        pygame.draw.line(
            _VARS['surf'], BLACK,
            (cont_x + (cellSize * x), cont_y),
            (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
    # # HORIZONTAl DIVISIONS
        pygame.draw.line(
            _VARS['surf'], BLACK,
            (cont_x, cont_y + (cellSize*x)),
            (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)


def checkEvents(BOARD, open_nodes):
    global CURR_VEHICLE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        # MOVE SELECTED VEHICLE LEFT OR UP DEPENDING ON ORIENTATION
        elif event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_UP):
            if(CURR_VEHICLE == -1):
                print("no vehicle")
            else:
                BOARD.moveVehicleLeftUp(CURR_VEHICLE, 1)
                # FOR TESTING NODE COST VALUES
                print("------------------------------------")
                for node in open_nodes:
                    print("_----------------------------------_")
                    print(node.state)
                    print(node.get_Fn())
        # MOVE SELECTED VEHICLE RIGHT OR DOWN DEPENDING ON ORIENTATION
        elif event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_DOWN):
            if(CURR_VEHICLE == -1):
                print("no vehicle")
            else:
                BOARD.moveVehicleRightDown(CURR_VEHICLE, 1)
                # FOR TESTING NODE COST VALUES
                print("------------------------------------")
                for node in open_nodes:
                    print("_----------------------------------_")
                    print(node.state)
                    print(node.get_Fn())
        # SELECT VEHICLE WITH ID BETWEEN 1 AND 9 WITH KEYS 1->9
        elif event.type == KEYDOWN and event.key >= K_1 and event.key <= K_9:
            CURR_VEHICLE = event.key - 48
        # VEHICLES WITH ID BETWEEN 10 AND 16 WITH KEYS A->F
        elif event.type == KEYDOWN and event.key >= 97 and event.key <= 102:
            CURR_VEHICLE = event.key - 87
        elif event.type == KEYDOWN and event.key == 103:
            BOARD.expandPossibleStates()


if __name__ == '__main__':
    main()
