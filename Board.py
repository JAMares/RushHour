import numpy as np
import random
from Vehicle import *


RED = (255, 0, 0)

COLOR_SELECTION = [(0, 0, 204), (0, 204, 204), (204, 204, 0),
                   (204, 102, 0), (153, 102, 0), (153, 0, 204),
                   (153, 204, 255), (102, 153, 0), (102, 102, 153),
                   (255, 153, 204), (153, 255, 51), (204, 153, 255),
                   (0, 51, 0), (153, 255, 204), (255, 204, 153)]

class Board:
    def __init__(self, gridSize, goal, puzzleFile):
        self.boardMAP = np.zeros((gridSize, gridSize), dtype=int)
        self.goalPos = goal
        self.vehicles = []
        self.colors = []
        self.mainPos = (0, 0)
        self.level = 0
        self.filePath = puzzleFile

    def hasWon(self):
        # CHECKS IF FRONT OF MAIN VEHICLE COLLIDES WITH GOAL POSITION
        if(self.mainPos[0]+1 == self.goalPos[0]):
            return True
        else:
            return False

    def checkCollision(self, vehicle):
        x = vehicle.position[0]
        y = vehicle.position[1]
        size = vehicle.size
        # CHECK ORIENTATION OF VEHICLE (VERTICAL OR HORIZONTAL)
        if(vehicle.orientation == "h"):
            # CHECKS FOR COLLISION WITH THE LEFT AND RIGHT BORDERS OF THE GAME BOARD
            if(x+size > self.boardMAP.shape[0] or x < 0):
                return True
            # CHECKS FOR COLLISIONS WITH EXISTING CARS IN THE GAME BOARD X AXIS
            for i in range(0, size):
                id = self.boardMAP[x+i][y]
                if(id != vehicle.identification and id != 0):
                    return True
        else:
            # CHECKS FOR COLLISION WITH THE TOP AND BOTTOM BORDERS OF THE GAME BOARD
            if(y+size > self.boardMAP.shape[1] or y < 0):
                return True
            # CHECKS FOR COLLISIONS WITH EXISTING CARS IN THE GAME BOARD Y AXIS
            for i in range(0, size):
                id = self.boardMAP[x][y+i]
                if(id != vehicle.identification and id != 0):
                    return True
        return False

    def resetBoard(self):
        # CLEARS VEHICLES
        self.vehicles.clear()
        # CLEARS BOARD
        self.boardMAP = np.zeros(
            (self.boardMAP.shape[0], self.boardMAP.shape[1]), dtype=int)
        # RESET MAIN POS
        self.mainPos = (0, 0)

    def generatePuzzle(self):
        # GENERATES RANDOM LIST CONTAINING 15 PRE-LOADED COLORS MINUS RED
        self.colors = random.sample(COLOR_SELECTION, 15)
        # CLEARS VARIABLE AND WIN STATE
        self.resetBoard()
        f = open(self.filePath, "r")
        list = f.read().split("\n")
        # CHECKS FOR AVAILABLE LEVELS
        if(len(list) > self.level):
            list = list[self.level].split(" ")
        else:
            return SystemExit(str("All levels complete"))
        # PREPARES FOR NEXT LEVEL
        self.level += 1
        for v in list:
            id = len(self.vehicles) + 1
            vehicle = Vehicle(id, 0, (int(
                v[0]), int(v[1])), int(v[2]), v[3])
            if(id == 1):  # FIRST VEHICLE IS ALWAYS THE MAIN ONE
                vehicle.color = RED  # FIRST VEHICLE ALWAYS RED
                self.mainPos = vehicle.position
            else:
                # MATCHES EACH VEHICLE ID WITH A COLOR FROM THE LIST
                vehicle.color = self.colors[id]

            # TEST TO VERIFY IF INSERTION OF VEHICLE HAPPENED WITHOUT COLLISIONS
            test = self.insertVehicle(vehicle)
            if(test == False):
                # THIS SHOULD BE CHANGED TO A POP-UP MESSAGE
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
        # PLACING VEHICLE IN NEW POSITION
        x = vehicle.position[0]
        y = vehicle.position[1]
        size = vehicle.size
        # CHECKS ORIENTATION
        if(vehicle.orientation == "h"):
            # PUTS VEHICLE ID (int > 0) AS VALUE OF CORRESPONDING GRID POSITION
            for i in range(0, size):
                # FOR LOOP ACCOUNTS FOR SIZE OF VEHICLE
                self.boardMAP[x+i][y] = vehicle.identification
        else:
            # PUTS VEHICLE ID (int > 0) AS VALUE OF CORRESPONDING GRID POSITION
            for i in range(0, size):
                # FOR LOOP ACCOUNTS FOR SIZE OF VEHICLE
                self.boardMAP[x][y+i] = vehicle.identification
        # CHECKS IF THIS IS THE MAIN VEHICLE AND UPDATES THE STORED POSITION
        if(vehicle.isMain == True):
            self.mainPos = vehicle.position

    def getVehicle(self, vehicleId):
        for vehicle in self.vehicles:
            if (vehicle.identification == vehicleId):
                return vehicle
        return -1

    def moveVehicleLeftUp(self, vehicleId, amount):
        vehicle = self.getVehicle(vehicleId)
        # COPIES OLD POSITION
        pos = (vehicle.position[0], vehicle.position[1])
        # CHECKS ORIENTATION OF VEHICLE
        if(vehicle.orientation == "v"):
            # MOVES VEHICLE UP
            vehicle.position = (pos[0], pos[1] - amount)
            if(self.checkCollision(vehicle) == False):
                # UPDATES BOARD IF NO COLLISIONS
                self.updateVehicle(vehicle)
                return True
            else:
                # IF COLLISION DETECTED POSITION STAYS THE SAME
                vehicle.position = pos
                return False
        else:
            # MOVES VEHICLE LEFT
            vehicle.position = (pos[0] - amount, pos[1])
            if(self.checkCollision(vehicle) == False):
                # UPDATES BOARD IF NO COLLISIONS
                self.updateVehicle(vehicle)
                return True
            else:
                # IF COLLISION DETECTED POSITION STAYS THE SAME
                vehicle.position = pos
                return False

    def moveVehicleRightDown(self, vehicleId, amount):
        vehicle = self.getVehicle(vehicleId)
        # CHECKS IF NEXT MOVEMENT IS WIN MOVEMENT
        if(vehicle.isMain == True and vehicle.position[0] == self.goalPos[0] - vehicle.size):
            # SETS UP WIN STATE
            self.mainPos = (self.mainPos[0]+1, self.mainPos[1])
            return True
        # COPIES OLD POSITION
        pos = (vehicle.position[0], vehicle.position[1])
        # CHECKS ORIENTATION OF VEHICLE
        if(vehicle.orientation == "v"):
            # MOVES VEHICLE DOWN
            vehicle.position = (pos[0], pos[1] + amount)
            if(self.checkCollision(vehicle) == False):
                # UPDATES BOARD IF NO COLLISIONS
                self.updateVehicle(vehicle)
                return True
            else:
                vehicle.position = pos
                return False
        else:
            # MOVES VEHICLE RIGHT
            vehicle.position = (pos[0] + amount, pos[1])
            if(self.checkCollision(vehicle) == False):
                # UPDATES BOARD IF NO COLLISIONS
                self.updateVehicle(vehicle)
                return True
            else:
                vehicle.position = pos
                return False

    def countObstaclesLeftUp(self, vehicleId):
        v = self.getVehicle(vehicleId)
        x1 = v.position[0]
        y1 = v.position[1]
        count = 0
        counted = []
        if(v.orientation == "h"):
            for i in range(0, x1):
                if(self.boardMAP[i][y1] != 0 and counted.count(self.boardMAP[i][y1]) == 0):
                    counted.append(self.boardMAP[i][y1])
                    count += 1
        else:
            for i in range(0, y1):
                if(self.boardMAP[x1][i] != 0 and counted.count(self.boardMAP[x1][i]) == 0):
                    counted.append(self.boardMAP[x1][i])
                    count += 1
        return (count, counted)

    def countObstaclesRightDown(self, vehicleId):
        v = self.getVehicle(vehicleId)
        x1 = v.position[0]
        y1 = v.position[1]
        count = 0
        counted = []
        if(v.orientation == "h"):
            for i in range(x1+v.size, self.boardMAP.shape[0]):
                if(self.boardMAP[i][y1] != 0 and counted.count(self.boardMAP[i][y1]) == 0):
                    counted.append(self.boardMAP[i][y1])
                    count += 1
        else:
            for i in range(y1+v.size, self.boardMAP.shape[1]):
                if(self.boardMAP[x1][i] != 0 and counted.count(self.boardMAP[x1][i]) == 0):
                    counted.append(self.boardMAP[x1][i])
                    count += 1
        return (count, counted)

    def calculateCurrentStateCost(self):
        res = self.countObstaclesRightDown(1)
        cost = res[0]
        for v in res[1]:
            res1 = self.countObstaclesLeftUp(v)
            res2 = self.countObstaclesRightDown(v)
            cost += res1[0] if res1[0] <= res2[0] and res1[0] != 0 else res2[0]
        return cost