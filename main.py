import pickle
import pandas as pd
import f1classes
import re
from IPython.core.debugger import set_trace


def create_drivers(driverdict=None):
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

    driverdb = pd.DataFrame(columns=['Name', 'Team', 'Name3'])
    for key in driverdict:
        if key != "DriverTable":
            driver = pd.DataFrame(
                [driverdict[key].name, driverdict[key].constructor, key],
                index=['Name', 'Team', 'Name3'])
            driverdb = driverdb.append(driver.transpose(), ignore_index=True)
    driverdict["DriverTable"] = driverdb


def create_constructors():
    pass


def pickle_drivers(driverdict, file=r'data\drivers.pkl'):
    pickle.dump(driverdict, open(file, "wb"))


def load_drivers(file=r'data\drivers.pkl'):
    global driverdict
    driverdict = pickle.load(open(file, 'rb'))


if __name__ == "__main__":
    # Use the below to create a drivers pickle to store their information
    # driverdict = create_drivers()
    # pickle_drivers(driverdict)
    pass