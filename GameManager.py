from Constructor import Constructor
from DataGatherer import DataGatherer
from Constructor import Constructor
from Driver import Driver
import datetime
import random
from random import randint, choice, seed
import copy
import math

dataGatherer = DataGatherer()
now = datetime.datetime.now()
seed(now.second)
constructors = []
freeDrivers = []
activeDrivers = []
driverIds = []
circuits = []
pointPositions = [25,18,15,12,10,8,6,4,2,1,]

def removeValuesFromList(list, val):
   return [value for value in list if value != val]

def printConstructor(constructor):
    print('id',constructor.constructorId)
    print('name',constructor.name)
    print('championship points',constructor.championshipPoints)
    print('speed points',constructor.speedPoints)
    for id in constructor.driverIds:
        print('driver',id)
    print()

def printDriver(driver):
    print('id',driver.driverId)
    print('name',driver.firstName, driver.surName)
    print('championship points', driver.championshipPoints)
    print('speed points', driver.speedPoints)
    print('constructor', driver.constructorId)
    print()

def printConstructors():
    for constructor in constructors:
        printConstructor(constructor)

def printDrivers(drivers):
    for driver in drivers:
        printDriver(driver)

def printDriverStandings():
    activeDrivers.sort(key=lambda driver: driver.championshipPoints, reverse=True)

    print('Driver Standings')
    print('Pos Name  Team   Points')
    for i,driver in enumerate(activeDrivers):
        print(i+1,driver.firstName,driver.surName, driver.constructorId, driver.championshipPoints)
    print()

def printConstructorStandings():
    constructors.sort(key=lambda constructor: constructor.championshipPoints, reverse=True)

    print('Constructors Standings')
    print('Pos Name   Points')
    for i,constructor in enumerate(constructors):
        print(i+1,constructor.name,constructor.championshipPoints)
    print()

def removeTeamless():
    popDrivers = []
    for driver in activeDrivers:
        if driver.constructorId == 'noTeam':
            popDrivers.append(driver)
        
    for driver in popDrivers:
        activeDrivers.remove(driver)
        freeDrivers.append(driver)

def addDriversToTeams():

    for constructor in constructors: 
        constructor.driverIds = []

    for constructor in constructors:
        for driver in activeDrivers:
            if constructor.constructorId == driver.constructorId:
                ##this way of resolving a teams too many drivers problem may lead to a reserve being assumed as a main driver if they outperform a main driver
                if constructor.driverIds.__len__() <= 1 :
                    constructor.driverIds.append(driver.driverId)
                    driver.speedPoints += constructor.speedPoints
                else:
                    driver.constructorId = 'noTeam'
    removeTeamless()
        
def processRaceResults(raceOrder):
    i = 0
    for driverId in raceOrder:
        
        for driver in activeDrivers:
            if driver.driverId == driverId:
                print(i+1,driver.firstName,driver.surName,driver.constructorId)
                if i <= 9:
                    points = pointPositions[i]
                    driver.championshipPoints += points
                    driver.speedPoints += points
                    for constructor in constructors:
                        if constructor.driverIds.__contains__(driverId):
                            constructor.championshipPoints += points
                            constructor.speedPoints += int(points/2)
                            for driver in activeDrivers:
                                if constructor.constructorId == driver.constructorId:
                                    driver.speedPoints += int(points/2)

            
        i += 1
    print()

def doRace(raceNumber,racesThisSeason):
    print('Race',raceNumber,'/',racesThisSeason,'at',random.choice(circuits), 'Final Result')
    raceList = []
    finishOrder = []
    for driver in activeDrivers:
        for _ in range(0,driver.speedPoints):
            raceList.append(driver.driverId)

    for p in range(0,activeDrivers.__len__()):
        driverId = random.choice(raceList)
        raceList = removeValuesFromList(raceList, driverId)
        finishOrder.append(driverId)
    #print(finishOrder)
    processRaceResults(finishOrder)

def resolveRetirements():
    for i,driver in enumerate(activeDrivers):
        pos = i+1
        retirementChance = pos
        if(randint(0,100) <= retirementChance):
            #print(driver.firstName,driver.surName, 'retires from the sport')
            driver.constructorId = 'noTeam'
            #freeDrivers.append(activeDrivers.pop(activeDrivers.index(driver)))
            for constructor in constructors:
                if constructor.driverIds.__contains__(driver.driverId):
                    constructor.driverIds.remove(driver.driverId)

def driversLeaveTeams():
    for x,constructor in enumerate(constructors):
        cp = x+1
        for y,driver in enumerate(activeDrivers):
            dp = y+1
            if constructor.driverIds.__contains__(driver.driverId):
                if (int(math.ceil(dp/2))) < cp :
                    if randint(0,10) >= 5:
                        driver,constructor = removeDriverFromConstructor(driver,constructor)



def removeDriverFromConstructor(driver,constructor):
    constructor.driverIds.remove(driver.driverId)
    driver.constructorId = 'noTeam'
    #print(driver.firstName,driver.surName,'and',constructor.name,'part ways')
    return driver,constructor

def addDriverToConstructor(driver,constructor):
    constructor.driverIds.append(driver.driverId)
    driver.constructorId = constructor.constructorId
    #print(constructor.name,'hires',driver.firstName,driver.surName)
    return driver,constructor

def constructorsFireDrivers():
    for x,constructor in enumerate(constructors):
        cp = x+1
        for y,driver in enumerate(activeDrivers):
            dp = y+1
            if constructor.driverIds.__contains__(driver.driverId):
                if cp*2 < dp :
                    if randint(0,10) >= 5:
                        driver,constructor = removeDriverFromConstructor(driver,constructor)

def constructorsHireDrivers():
    allHaveTwo = False
    i = 0
    while (not allHaveTwo) or (i == 0):
        i += 1
        allHaveTwo = True
        for x,constructor in enumerate(constructors):
            #print(constructor.name,'choose a driver')
            cp = x+1
            roundswithoutdriver = 0
            while constructor.driverIds.__len__() < 2:
                for y,driver in enumerate(activeDrivers):
                    dp = y+1
                    if (int(cp*2) >= dp) or (roundswithoutdriver > 0):
                        if driver.constructorId == 'noTeam' :
                            driver,constructor = addDriverToConstructor(driver,constructor)
                    '''else:
                        if not (constructor.driverIds.__contains__(driver.driverId)):
                            if randint(0,100) > cp*11:
                                for oldConstructor in constructors:
                                    if oldConstructor.driverIds.__contains__(driver.driverId):
                                        driver,oldConstructor = removeDriverFromConstructor(driver,oldConstructor)
                                        allHaveTwo = False
                                        driver,constructor = addDriverToConstructor(driver,constructor)'''
                if (constructor.driverIds.__len__() < 2) and freeDrivers.__len__() > 0:
                    driverIndex = freeDrivers.index(random.choice(freeDrivers))
                    driver = freeDrivers.pop(driverIndex)
                    #print(driver.firstName,driver.surName,'(re)Joins the sport')
                    driver,constructor = addDriverToConstructor(driver,constructor)
                    activeDrivers.append(driver)
                roundswithoutdriver += 1

def setDriverSpAndChPostSeason(drivers):
    for driver in drivers:
            driver.speedPoints = int(driver.championshipPoints/2) + 10
            driver.championshipPoints = 0

def setConstructorSpAndChPostSeason(constructors):
    for constructor in constructors:
        constructor.speedPoints = int(constructor.championshipPoints/2)
        constructor.championshipPoints = 0

def setSpAndCh():
    setDriverSpAndChPostSeason(freeDrivers)
    setDriverSpAndChPostSeason(activeDrivers)
    setConstructorSpAndChPostSeason(constructors)
    addDriversToTeams()
    
def postSeasonUpdate(oldDrivers):
    #print('old')
    #printDrivers(oldDrivers)
    #print('new')
    #printDrivers(activeDrivers)
    for oldDriver in oldDrivers:
        leftSport = True
        for driver in activeDrivers:
            if oldDriver.driverId == driver.driverId:
                leftSport = False
                if oldDriver.constructorId != driver.constructorId:
                    print(oldDriver.firstName,oldDriver.surName,'moved from',oldDriver.constructorId,'to',driver.constructorId)
        if leftSport:
            print(oldDriver.firstName,oldDriver.surName,'Left',oldDriver.constructorId, 'and the sport')
    for driver in activeDrivers:
        joinedSport = True
        for oldDriver in oldDrivers:
            if oldDriver.driverId == driver.driverId:
                joinedSport = False
        if joinedSport:
            print(driver.firstName,driver.surName,'is a rookie with',driver.constructorId)



def postSeason():
    cloneDrivers = copy.deepcopy(activeDrivers)
    resolveRetirements()
    constructorsFireDrivers()
    driversLeaveTeams()
    constructorsHireDrivers()
    setSpAndCh()
    postSeasonUpdate(cloneDrivers)


print('what year would you like the starting lineup to be from?')
startYear = int(input())
print('what year would you like to start pulling reserve drivers from max', now.year)
pullYearOne = int(input())
print('what year would you like to end pulling reserve drivers from min 1950')
pullYearTwo = int(input())

activeDrivers,driverIds= dataGatherer.pullDriversFromYear(startYear,activeDrivers,driverIds)
##THIS ADDS ADAM AS A JOKE
adam = Driver('adam_ralston', 'Adam', 'Ralston', 100, 'noTeam')
freeDrivers.append(adam)
##THIS ADDS SEAN AS A JOKE
sean = Driver('sean_crancher', 'Sean', 'Crancher', 100, 'noTeam')
freeDrivers.append(sean)
for i in range(pullYearOne,pullYearTwo-1,-1):
    freeDrivers,driverIds= dataGatherer.pullDriversFromYear(i,freeDrivers,driverIds)
for driver in freeDrivers:
    driver.constructorId = 'noTeam'
constructors = dataGatherer.pullConstructorsFromYear(startYear,constructors)
circuits = dataGatherer.pullCircuits(circuits)
addDriversToTeams()
while True:
    racesThisSeason = randint(0,24) + 1
    print('there will be',racesThisSeason,'race(s) this season')
    print()
    for i in range(0,racesThisSeason):
        printConstructorStandings()
        printDriverStandings()
        input()
        doRace(i+1,racesThisSeason)
        input()
    print('Seasons Final Standings')
    printConstructorStandings()
    printDriverStandings()
    postSeason()
    input()


    #printDrivers(activeDrivers)
    #printConstructors()
    #print(driverIds)