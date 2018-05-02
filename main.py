import pickle
import pandas as pd
import f1classes
import re
from IPython.core.debugger import set_trace


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


def pickle_drivers(driverdict, file=r'data\drivers.pkl'):
    """
    Pickles the driversdict
    
    Parameters
    ----------
    driverdict : dict
        Dictionary of driver objects
    file : string, optional
        File path to pickle to (the default is r'data\drivers.pkl')
    
    """

    pickle.dump(driverdict, open(file, "wb"))


def pickle_constructors(constructordict, file=r'data\constructors.pkl'):
    """
    Pickles the constructorsdict
    
    Parameters
    ----------
    constructordict : dict
        Dictionary of constructor objects
    file : string, optional
        File path to pickle to (the default is r'data\constructors.pkl')
    
    """

    pickle.dump(constructordict, open(file, "wb"))


def load_constructors(file=r'data\constructors.pkl'):
    """
    Loads the constructordict from pickle. Default location is the standard position for the dictionary pickle
    
    file : string, optional
        Path to pickled file (the default is r'data\constructors.pkl')
    
    """

    global constructordict
    constructordict = pickle.load(open(file, 'rb'))


def load_drivers(file=r'data\drivers.pkl'):
    """
    Loads the driverdict from pickle. Default location is the standard position for the dictionary pickle.
    
    file : string, optional
        Path to pickled file (the default is r'data\drivers.pkl')
    
    """

    global driverdict
    driverdict = pickle.load(open(file, 'rb'))


if __name__ == "__main__":
    # Use the below to create a drivers pickle to store their information
    # driverdict = create_drivers()
    # pickle_drivers(driverdict)
    pass