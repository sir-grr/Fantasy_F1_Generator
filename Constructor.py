from Driver import Driver
class Constructor:
    def __init__(self,points,constructorId,constructorName):
        self.speedPoints = int(int(points)/2)
        self.championshipPoints = 0
        self.constructorId = constructorId
        self.name = constructorName
        self.driverIds = []

    