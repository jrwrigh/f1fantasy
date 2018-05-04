import namedtupled
import requests
import re
import datetime
from warnings import warn
import pandas as pd
from IPython.core.debugger import set_trace


class driver(object):

    def __init__(self, name, constructor, name3):
        self.name = name
        self.constructor = constructor
        self.name3 = name3

    def create_profile(self, quali=None, race=None, fantasy=None, cost=None):
        """
        Creation of driver profile data
        
        Parameters
        ----------
        quali : DataFrame
            Qualifying Results
        race : DataFrame
            Race Results
        fantasy : DataFrame
            Fantasy scores
        cost : DataFrame
            Cost history information about the driver
        """
        self.quali = quali
        self.race = race
        self.fantasy = fantasy
        self.cost = cost

    def update_data(self, type, round=None, year=None):
        """
        Updates the driver profile data.
        
        Parameters
        ----------
        type : string
            Which data set will be updated. Either "quali", "race", or "fantasy"
        round : string or int
            Says which round of the season it should update. If "None" the next 
            round without data will be filled. Default is "None"
        year : int
            Says which season should be updated. Default is "None". If "None" 
            assumes current season.
        """

    #This is TBD for now
    pass


class constructor(object):

    def __init__(self, constructor, drivers):
        self.constructor = constructor
        self.drivers = drivers

    def create_profile(self, quali, race, fantasy, cost):
        """
        Creation of constructor data
        
        Parameters
        ----------
        quali : DataFrame
            Qualifying results
        race : DataFrame
            Race results
        fantasy : DataFrame
            Fantasy Scores
        cost : DataFrame
            Cost history information about the driver
        """
        self.quali = quali
        self.race = race
        self.fantasy = fantasy
        self.cost = cost


class RaceWeekend(object):

    def __init__(self, season=None, roundn=None, initialize=True):
        self.rawr = None
        self.rawq = None
        if roundn == 'latest' and initialize:
            self.init_from_ergast()
            self.parse_raceresults()
            self.parse_qualiresults()
        elif season and roundn:
            self.init_from_ergast(season, roundn)
            self.parse_raceresults()
            self.parse_qualiresults()

# Baharain race (round 2) has a not attribute 'FastestLap' with a driver for some reason
    def init_from_ergast(self, season=None, roundn=None):
        url_base = r'https://ergast.com/api/f1'
        if not season or not roundn:
            urlr = url_base + '/current/last/results' + '.json'
        elif season and roundn:
            urlr = url_base + '/' + str(season) + '/' + str(roundn) + '/results.json'
        rawjson = requests.get(urlr).json()
        self.rawr = namedtupled.map(rawjson)
        self.Raceraw = self.rawr.MRData.RaceTable.Races[0]

        if not season or not roundn:
            urlq = url_base + '/' + self.Raceraw.season + '/' + self.Raceraw.round + '/qualifying.json'
        elif season and roundn:
            urlq = url_base + '/' + str(season) + '/' + str(roundn) + '/qualifying.json'
 
        rawjson_quali = requests.get(urlq).json()
        self.rawq = namedtupled.map(rawjson_quali)
        self.Qualiraw = self.rawq.MRData.RaceTable.Races[0]

        self.season = int(self.Raceraw.season)
        self.roundn = int(self.Raceraw.round)
        self.raceName = self.Raceraw.raceName
        dateraw = re.match(r'(\d{4})-(\d{2})-(\d{2})', self.Raceraw.date)
        self.date = datetime.date(
            int(dateraw.group(1)), int(dateraw.group(2)), int(dateraw.group(2)))
        # TODO add qualifying stuff
        # http://ergast.com/mrd/methods/qualifying/

    def parse_raceresults(self):
        if self.rawr == None:
            raise Exception('Raw data has not been imported yet')
        Results = self.Raceraw.Results
        ResultsTable = pd.DataFrame(columns=[
            'Position', 'Name', 'Name3', 'Grid', 'Fastest Lap', 'Constructor',
            'Status', 'Change'
        ])
        for result in Results:
            driver = {}
            driver['Position'] = int(result.position)
            driver[
                'Name'] = result.Driver.givenName + ' ' + result.Driver.familyName
            driver['Name3'] = result.Driver.code
            # if result.FastestLap.rank == 1:
            #     driver['Fastest Lap'] = True
            # else:
            #     driver['Fastest Lap'] = False
            if result.laps != '0':
                driver[
                    'Fastest Lap'] = True if result.FastestLap.rank == '1' else False
            driver['Constructor'] = result.Constructor.name
            driver['Grid'] = int(result.grid)
            driver['Status'] = result.status
            driver['Change'] = driver['Grid'] - driver['Position']

            ResultsTable = ResultsTable.append(driver, ignore_index=True)
        self.RaceResultsTable = ResultsTable

    def parse_qualiresults(self):
        if self.rawq == None:
            raise Exception('Raw data has not been imported yet')
        Results = self.Qualiraw.QualifyingResults
        ResultsTable = pd.DataFrame(columns=['Position','Name','Name3','Constructor','Q1','Q2','Q3'])

        for result in Results:
            driver = {}
            driver['Position'] = int(result.position)
            driver[
                'Name'] = result.Driver.givenName + ' ' + result.Driver.familyName
            driver['Name3'] = result.Driver.code
            driver['Constructor'] = result.Constructor.name

            if result.Q1 == '':
                driver.update({'Q1':False,'Q2':False,'Q3':False})
            elif result.Q1 != '':
                if hasattr(result, 'Q2'):
                    if hasattr(result, 'Q3'):
                        driver.update({'Q1':True,'Q2':True,'Q3':True})
                    else:
                        driver.update({'Q1':True,'Q2':True,'Q3':False})
                else:
                    driver.update({'Q1':True,'Q2':False,'Q3':False})


            ResultsTable = ResultsTable.append(driver, ignore_index=True)
        self.QualiResultsTable = ResultsTable
