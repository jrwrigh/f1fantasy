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

    def __init__(self):
        # self.raw = None
        pass

    def init_from_ergast(self, season=None, roundn=None):
        url_base = r'https://ergast.com/api/f1'
        url_suffix_latest = r'/current/last/results'
        if not season or roundn:
            url = url_base + url_suffix_latest + '.json'
        rawjson = requests.get(url).json()
        self.raw = namedtupled.map(rawjson)
        self.Raceraw = self.raw.MRData.RaceTable.Races[0]

        self.season = int(self.Raceraw.season)
        self.roundn = int(self.Raceraw.round)
        self.raceName = self.Raceraw.raceName
        dateraw = re.match(r'(\d{4})-(\d{2})-(\d{2})',
                           self.Raceraw.date)

        self.date = datetime.date(
            int(dateraw.group(1)), int(dateraw.group(2)), int(dateraw.group(2)))

    def parse_raceresults(self):
        try:
            self.raw != None
        except:
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
            driver['Change'] = driver['Position'] - driver['Grid']

            ResultsTable = ResultsTable.append(driver, ignore_index=True)
        self.ResultsTable = ResultsTable