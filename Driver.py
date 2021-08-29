class Driver:
    def __init__(self, driverId, firstName, surName, points, constructorId):

        self.driverId = driverId
        self.firstName = firstName
        self.surName = surName
        self.championshipPoints = 0
        self.speedPoints = int(int(points)/2) + 10
        self.constructorId = constructorId
    