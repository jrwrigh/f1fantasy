
class driver(object):

    def __init__(self, driver, constructor):

        self.driver = driver
        self.constructor = constructor

    def create_profile(self, quali, race, fantasy, cost):
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
        self.quali = qual
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
            Says which round of the season it should update. If "None" the next round without data will be filled. Default is "None"
        year : int
            Says which season should be updated. Default is "None". If "None" assumes current season.
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




