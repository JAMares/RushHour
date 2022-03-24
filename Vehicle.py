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