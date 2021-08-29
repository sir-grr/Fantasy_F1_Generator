import requests
import json
import datetime
from Driver import Driver
from Constructor import Constructor

class DataGatherer:
    #method for getting drivers from a given year that are not already in our list
    def pullDriversFromYear(self,year, drivers, driverIds):
        print('getting drivers from',year)
        baseUrl = 'http://ergast.com/api/f1/{}/driverStandings.json'
        url = baseUrl.format(year)
        r = requests.get(url)
        results = r.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        for entry in results:
            driverId = entry['Driver']['driverId']
            if(not (driverIds.__contains__(driverId))):
                driverIds.append(driverId)
                currentDriver = Driver(driverId, entry['Driver']['givenName'], entry['Driver']['familyName'], int(float(entry['points'])), entry['Constructors'][0]['constructorId'])
                drivers.append(currentDriver)
                #print(currentDriver.firstName,currentDriver.surName,currentDriver.championshipPoints,currentDriver.id)
        return drivers,driverIds

    '''
    print('input the year you want drivers from')
    driverYear = int(input())

    pullDriversFromYear(driverYear)

    '''

    #adding the current years drivers
    #pullDriversFromYear(now.year)
    #adding in drivers from every other year
    #for i in range(now.year - 1, 1950 - 1, -1):
    #    pullDriversFromYear(i)
    def pullConstructorsFromYear(self,year, constructors):
        print('getting constructors from',year)
        baseUrl = 'http://ergast.com/api/f1/{}/constructorStandings.json'
        url = baseUrl.format(year)
        r = requests.get(url)
        results = r.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        for entry in results:
            currentConstructor = Constructor(int(float(entry['points'])), entry['Constructor']['constructorId'], entry['Constructor']['name'])
            constructors.append(currentConstructor)
            #print(currentConstructor.speedPoints, currentConstructor.name, currentConstructor.id)
        return constructors

    def pullCircuits(self,circuits):
        url = 'http://ergast.com/api/f1/circuits.json'
        r = requests.get(url)
        results = r.json()['MRData']['CircuitTable']['Circuits']
        #print(results)
        for entry in results:
            circuit = entry['circuitName']
            circuits.append(circuit)
        return circuits
