
from pickle import REDUCE
import random
import string
import sys
import pygame
from pygame.locals import KEYDOWN, K_q, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_1, K_9
import numpy as np
# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (160, 160, 160)

COLOR_SELECTION = [(0, 0, 204), (0, 204, 204), (204, 204, 0),
                   (204, 102, 0), (153, 102, 0), (153, 0, 204),
                   (153, 204, 255), (102, 153, 0), (102, 102, 153),
                   (255, 153, 204), (153, 255, 51), (204, 153, 255),
                   (0, 51, 0), (153, 255, 204), (255, 204, 153)]


class Vehicle:
    def __init__(self, id, col, pos, size, orientation):
        self.identification = id
        self.color = col
        self.position = pos
        self.size = size
        self.orientation = orientation
        self.isMain = False
        if(id == 1):
            self.isMain = True


class Board:
    def __init__(self, gridSize, goal):
        self.boardMAP = np.zeros((gridSize, gridSize), dtype=int)
        self.goalPos = goal
        self.vehicles = []
        self.colors = []
        self.mainPos = (0, 0)

    def hasWon(self):
        if(self.mainPos[0]+1 == self.goalPos[0]):
            return True
        else:
            return False

    def checkCollision(self, vehicle):
        x = vehicle.position[0]
        y = vehicle.position[1]
        size = vehicle.size
        if(vehicle.orientation == "h"):
            if(x+size > self.boardMAP.shape[0] or x < 0):
                return True
            for i in range(0, size):
                id = self.boardMAP[x+i][y]
                if(id != vehicle.identification and id != 0):
                    return True
        else:
            if(y+size > self.boardMAP.shape[1] or y < 0):
                return True
            for i in range(0, size):
                id = self.boardMAP[x][y+i]
                if(id != vehicle.identification and id != 0):
                    return True
        return False

    def generatePuzzle(self, filePath):
        self.colors = random.sample(COLOR_SELECTION, 15)
        f = open(filePath, "r")
        list = f.read().split(" ")
        for v in list:
            id = len(self.vehicles) + 1
            vehicle = Vehicle(id, 0, (int(
                v[0]), int(v[1])), int(v[2]), v[3])
            if(id == 1):
                vehicle.color = RED
                self.mainPos = vehicle.position
            else:
                vehicle.color = self.colors[id]

            test = self.insertVehicle(vehicle)
            if(test == False):
                raise SystemExit(str("Vehicle collision detected"))

    def insertVehicle(self, vehicle):
        if(self.checkCollision(vehicle) == False):
            self.updateVehicle(vehicle)
            self.vehicles.append(vehicle)
            return True
        else:
            return False

    def updateVehicle(self, vehicle):
        # CLEAN OLD VEHICLE POSITION
        for i in range(0, self.boardMAP.shape[0]):
            for j in range(0, self.boardMAP.shape[1]):
                if(self.boardMAP[i][j] == vehicle.identification):
                    self.boardMAP[i][j] = 0
        # PLACE VEHICLE IN NEW POSITION
        x = vehicle.position[0]
        y = vehicle.position[1]
        size = vehicle.size
        if(vehicle.orientation == "h"):
            for i in range(0, size):
                self.boardMAP[x+i][y] = vehicle.identification
        else:
            for i in range(0, size):
                self.boardMAP[x][y+i] = vehicle.identification
        if(vehicle.isMain == True):
            self.mainPos = vehicle.position

    def getVehicle(self, vehicleId):
        for vehicle in self.vehicles:
            if (vehicle.identification == vehicleId):
                return vehicle
        return -1

    def moveVehicleLeftUp(self, vehicleId, amount):
        vehicle = self.getVehicle(vehicleId)
        pos = (vehicle.position[0], vehicle.position[1])
        if(vehicle.orientation == "v"):
            vehicle.position = (pos[0], pos[1] - amount)
            if(self.checkCollision(vehicle) == False):
                self.updateVehicle(vehicle)
                return True
            else:
                vehicle.position = pos
                return False
        else:
            vehicle.position = (pos[0] - amount, pos[1])
            if(self.checkCollision(vehicle) == False):
                self.updateVehicle(vehicle)
                return True
            else:
                vehicle.position = pos
                return False

    def moveVehicleRightDown(self, vehicleId, amount):
        vehicle = self.getVehicle(vehicleId)
        # CHECKS IF NEXT MOVEMENT IS WIN MOVEMENT
        if(vehicle.isMain == True and vehicle.position[0] == self.goalPos[0] - vehicle.size):
            # SETS UP WIN STATE
            self.mainPos = (self.mainPos[0]+1, self.mainPos[1])
            return True
        pos = (vehicle.position[0], vehicle.position[1])
        if(vehicle.orientation == "v"):
            vehicle.position = (pos[0], pos[1] + amount)
            if(self.checkCollision(vehicle) == False):
                self.updateVehicle(vehicle)
                return True
            else:
                vehicle.position = pos
                return False
        else:
            vehicle.position = (pos[0] + amount, pos[1])
            if(self.checkCollision(vehicle) == False):
                self.updateVehicle(vehicle)
                return True
            else:
                vehicle.position = pos
                return False


_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': 0, 'lineWidth': 2}
global CURR_VEHICLE
BOARD = Board(6, (6, 2))


def main():
    global CURR_VEHICLE
    CURR_VEHICLE = -1
    pygame.init()

    BOARD.generatePuzzle("./problems.txt")

    _VARS['gridCells'] = BOARD.boardMAP.shape[0]

    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawSquareGrid(
            _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
        placeCells()
        pygame.display.update()
        if(BOARD.hasWon() == True):
            print("GAME WON")
            return


# NEW METHOD FOR ADDING CELLS :
def placeCells():
    # GET CELL DIMENSIONS...
    cellBorder = 6
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    # DOUBLE LOOP
    for row in range(BOARD.boardMAP.shape[0]):
        for column in range(BOARD.boardMAP.shape[1]):
            # Is the grid cell tiled ?
            if(BOARD.boardMAP[row][column] != 0):
                # print((row, column))
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
    # WIN CELL
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


def checkEvents():
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
        # MOVE SELECTED VEHICLE RIGHT OR DOWN DEPENDING ON ORIENTATION
        elif event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_DOWN):
            if(CURR_VEHICLE == -1):
                print("no vehicle")
            else:
                BOARD.moveVehicleRightDown(CURR_VEHICLE, 1)
        # SELECT VEHICLE WITH ID BETWEEN 1 AND 9
        elif event.type == KEYDOWN and event.key >= K_1 and event.key <= K_9:
            CURR_VEHICLE = event.key - 48


if __name__ == '__main__':
    main()
