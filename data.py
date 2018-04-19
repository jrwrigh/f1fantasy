
class driver(object):

    def __init__(self, driver, constructor):

        self.driver = driver
        self.constructor = constructor

    def create_profile(self, quali, race, fantasy):
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
        """
        self.quali = quali
        self.race = race
        self.fantasy = fantasy

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



