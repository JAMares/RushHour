from asyncio.windows_events import NULL
from pickle import REDUCE
import sys
import copy
import time
import pygame
from tkinter import *
from tkinter import messagebox
from pygame.locals import KEYDOWN, K_q, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_1, K_9
from Board import *
from Graph import *
from Button import *
import threading
from openFile import *

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (160, 160, 160)


# SCREEN DATA
_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': 0, 'lineWidth': 2}
# CURRENT SELECTED VEHICLE
global CURR_VEHICLE
# INITIALIZES GAME BOARD, WIN POS AT x:6, y:2 (OUTSIDE MAIN PLAY AREA)


def createNodes(node: Node, board, openNodes, closeNodes):
    movementCount = node.movements+1
    board.boardMAP = node.state
    board.vehicles = node.vehicles
    possibleStates = board.expandPossibleStates()
    # THIS ALREADY CHECKS IF EACH NODE STATE DOESN'T EXIST ALREADY
    for index in range(0, len(possibleStates[0])):
        board.boardMAP = possibleStates[0][index]
        board.vehicles = possibleStates[1][index]
        hCost = board.calculateCurrentStateCost()
        newNode = Node(node, movementCount, hCost,
                       board.boardMAP, board.vehicles)
        if checkNodeRepetition(newNode, openNodes) == False:
            if(checkNodeRepetition(newNode, closeNodes) == False):
                openNodes.append(newNode)

    # SORTS NODES BASED ON COST
    openNodes = sorted(openNodes, key=lambda node: node.get_Fn())
    return openNodes

# Function to insert open nodes avoiding repetitions


def checkNodeRepetition(newNode, nodeList):
    maxR = len(newNode.vehicles)
    for node in nodeList:
        test = False
        for index in range(0, maxR):
            if(node.vehicles[index].position != newNode.vehicles[index].position):
                break
            if(index == maxR-1):
                test = True
        if(test):
            return test
    # Depending on the intent, this could be changed to an ordered insert
    return False

# Function to check if a node was already considerate before


def a_estrella(root: Node, open_nodes, close_nodes, GAMEBOARD):
    currentNode = root
    open_nodes.append(currentNode)
    while (currentNode.blocked > 0):
        currentNode = open_nodes.pop(0)
        open_nodes = createNodes(
            currentNode, GAMEBOARD, open_nodes, close_nodes)
        close_nodes.append(currentNode)
    solution = []
    while(currentNode != 0):
        solution.append(currentNode)
        currentNode = currentNode.father
    solution.reverse()
    return solution

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
                drawSquareCell(x-5, y-5, celldimX+11, celldimY+11, v.color)

                # DRAWING CORRESPONDING ID FOR EACH VEHICLE CELL
                font = pygame.font.SysFont('arial', 20)
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
                            * cellBorder) + _VARS['lineWidth']/2 - 5,
            _VARS['gridOrigin'][1] + (celldimX*BOARD.goalPos[1])
            + cellBorder + (2*BOARD.goalPos[1]*cellBorder) +
            _VARS['lineWidth']/2 - 5,
            celldimX + 11, celldimY + 11, GREEN)


# Draw filled rectangle at coordinates

def drawButton(buttonStart):
    # elevation logic
    buttonStart.top_rect.y = buttonStart.y - buttonStart.elevation
    buttonStart.text_rect.center = buttonStart.top_rect.center

    buttonStart.bottom_rect.midtop = buttonStart.top_rect.midtop
    buttonStart.bottom_rect.height = buttonStart.top_rect.height + buttonStart.movement

    pygame.draw.rect(_VARS['surf'], buttonStart.bottom_color,
                     buttonStart.bottom_rect, border_radius=12)
    pygame.draw.rect(_VARS['surf'], buttonStart.top_color,
                     buttonStart.top_rect, border_radius=12)
    _VARS['surf'].blit(buttonStart.text, buttonStart.text_rect)


def check_click(buttonStart):
    while(1):
        mouse_pos = pygame.mouse.get_pos()
        if buttonStart.top_rect.collidepoint(mouse_pos):
            buttonStart.top_color = (0, 86, 31)
            if pygame.mouse.get_pressed()[0]:
                buttonStart.movement = 0
                buttonStart.pressed = True
                return True
            else:
                buttonStart.movement = buttonStart.elevation
                if buttonStart.pressed == True:
                    buttonStart.pressed = False
        else:
            buttonStart.movement = buttonStart.elevation
            buttonStart.top_color = (0, 140, 51)


def drawSquareCell(x, y, dimX, dimY, color):
    i = 0
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

# Verifica que los eventos le den click


def checkEvents(BOARD, solution, pos_solution, buttonStart):
    global CURR_VEHICLE
    if(pos_solution < len(solution)):
        BOARD.boardMAP = solution[pos_solution].state
    else:
        BOARD.moveVehicleMain()
    time.sleep(0.7)  # Here going to change for clickbutton
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == 103:
            BOARD.expandPossibleStates()

def RushH(file):
    global CURR_VEHICLE, buttonStart, isRunning

    # NO SELECTED VEHICLE
    CURR_VEHICLE = -1
    isRunning = 0
    # FILE PATH SELECTION SHOULD BE WITHIN INTERFACE
    GAMEBOARD = Board(6, "./problem1.txt")
    GAMEBOARD.generatePuzzle()

    open_nodes = []
    close_nodes = []
    length_solucion = 0

    father_node = Node(
        NULL, 0, GAMEBOARD.calculateCurrentStateCost(), GAMEBOARD.boardMAP, copy.deepcopy(GAMEBOARD.vehicles))
    test = a_estrella(father_node, open_nodes, close_nodes, GAMEBOARD)

    pygame.init()

    _VARS['gridCells'] = GAMEBOARD.boardMAP.shape[0]

    pygame.display.set_caption('Rush Hour')
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    buttonStart = Button('Start', 100, 30)
    tr = threading.Thread(target=check_click, args=(buttonStart,))
    tr.start()

    while True:
        checkEvents(GAMEBOARD, test, length_solucion, buttonStart)
        _VARS['surf'].fill(GREY)
        if (tr.is_alive()):
            drawButton(buttonStart)
        drawSquareGrid(
            _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
        placeCells(GAMEBOARD)
        pygame.display.update()
        if (tr.is_alive() == False):
            isRunning = 1
        # CHECKS FOR WIN STATE
        if(length_solucion < len(test) and isRunning == 1):
            length_solucion += 1
        if(GAMEBOARD.hasWon() == True):
            Tk().wm_withdraw()  # to hide the main window
            # answer saves what user wants (yes, no)
            answer = messagebox.askquestion(title="WIN",
                                            message="Congrats! Do yo want to continue to next level?")
            # Se debe pasar al sig nivel
            if(answer=='yes'):
                mainFile()
                pygame.quit()
                return
                
            else:
                RushH(file)
                
            #print(answer)
            #mainFile()
            #pygame.quit()
                
            # GOES TO NEXT LEVEL
            # GAMEBOARD.generatePuzzle()

            # NEW METHOD FOR ADDING CELLS :
