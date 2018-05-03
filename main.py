import dill
import pandas as pd
import f1classes
from IPython.core.debugger import set_trace
import pathlib 


def create_drivers(driverdict=None):
    """
    Function for creating the drivers dictionary and the driver objects that make it up
    
    driverdict : dict, optional
        When appending new drivers to the dictionary, this is the dictionary that the drivers will be appended to. (the default is None, which will create a new dictionary and return it)
    
    Returns
    -------
    dict
        The dictionary of drivers, whose key is the three letter drivers code and whose value is the driver object corresponding to the drivers code. ie the key "VET" has Sebastian Vettel's driver object as its value.
    """

    if not driverdict:
        driverdict = {}

    raw = pd.read_clipboard()
    for _, data in raw.iterrows():
        splitname = data['Name'].split(' ')
        if len(splitname) <= 2:
            name3 = splitname[1][0:3]
            name3 = name3.upper()

        driverobj = f1classes.driver(data['Name'], data['Team'], name3)
        driverdict[name3] = driverobj
    return (driverdict)


def add_DriverTable(driverdict):
    """
    Adds a DataFrame of the driver's information to the drivers dictionary. The DataFrame has the columns 'Name', 'Team', and 'Name3' where Name3 is the 3 letter driver code. It is placed in the driversdict under the key "DriverTable".
    
    Parameters
    ----------
    driverdict : dict
        The driversdict from which the DriverTable is built from and it then appended to.
    """

    driverdb = pd.DataFrame(columns=['Name', 'Team', 'Name3'])
    for key in driverdict:
        if key != "DriverTable":
            driver = pd.DataFrame(
                [driverdict[key].name, driverdict[key].constructor, key],
                index=['Name', 'Team', 'Name3'])
            driverdb = driverdb.append(driver.transpose(), ignore_index=True)
    driverdict["DriverTable"] = driverdb


def create_constructors(driverdict):
    """
    Function for creating constructors dictionary and its corresponding constructor objects. Information for the creation is taken from a driver dictionary that must be given.
    
    Parameters
    ----------
    driverdict : dict
        Driver dictionary used to make the constructors.
    """

    global constructordict
    constructordict = {}
    for _, driver in driverdict['DriverTable'].iterrows():
        Team = driver['Team']
        if Team not in constructordict.keys():
            drivers = driverdict['DriverTable'].loc[driverdict['DriverTable'][
                'Team'] == Team][['Name', 'Name3']]
            constructordict[Team] = f1classes.constructor(Team, drivers)


def pickle_drivers(driverdict, file='data/drivers.dill'):
    """
    Pickles the driversdict
    
    Parameters
    ----------
    driverdict : dict
        Dictionary of driver objects
    file : string, optional
        File path to pickle to (the default is 'data/drivers.dill')
    
    """

    file = pathlib.Path(file)
    dill.dump(driverdict, open(file, 'wb'))


def pickle_constructors(constructordict, file='data/constructors.dill'):
    """
    Pickles the constructorsdict
    
    Parameters
    ----------
    constructordict : dict
        Dictionary of constructor objects
    file : string, optional
        File path to pickle to (the default is 'data/constructors.dill')
    
    """

    file = pathlib.Path(file)
    dill.dump(constructordict, open(file, 'wb'))


def pickle_RaceWeekend(RaceWeekend, file=None):
    """
    Pickles a RaceWeekend object using dill.
    
    Parameters
    ----------
    RaceWeekend : f1classes.RaceWeekend
        Data for a Race Weekend
    file : str, optional
        File path to pickle to (the default is None, which places the file in 'data/races/' with the file format of '{season}_{roundn}-{country}.dill')
    
    """

    if file == None:
        file = pathlib.Path('data/races') / '{0}_{1}-{2}.dill'.format(
            RaceWeekend.season, RaceWeekend.roundn,
            RaceWeekend.Raceraw.Circuit.Location.country)
    dill.dump(RaceWeekend, open(file, 'wb')) 


def load_constructors(file='data/constructors.dill'):
    """
    Loads the constructordict from pickle. Default location is the standard position for the dictionary pickle
    
    file : string, optional
        Path to pickled file (the default is 'data\constructors.dill')
    
    """

    global constructordict
    file = pathlib.Path(file)
    constructordict = dill.load(open(file, 'rb'))

global driverdict
def load_drivers(file='data/drivers.dill'):
    """
    Loads the driverdict from pickle. Default location is the standard position for the dictionary pickle.
    
    file : string, optional
        Path to pickled file (the default is 'data\drivers.dill')
    
    """

    global driverdict
    file = pathlib.Path(file)
    driverdict = dill.load(open(file, 'rb'))

def load_RaceWeekend(filepath=None, season=None, roundn=None, country=None):
    """
    Loads a RaceWeekend object into the namespace using dill
    
    filepath : str, optional
        Path to the pickled file (the default is None)
    season : int, optional
        The season of the race (the default is None)
    roundn : int, optional
        The round number of the race (the default is None)
    country : str, optional
        The country location of the race (the default is None)
    
    """

    path = pathlib.Path('data/races')
    if filepath:
        file = pathlib.Path(filepath)
    
    return(dill.load(open(file, 'rb')))


if __name__ == '__main__':
    # Use the below to create a drivers pickle to store their information
    # driverdict = create_drivers()
    # pickle_drivers(driverdict)
    pass