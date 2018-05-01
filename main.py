import pickle
import pandas as pd
import f1classes
import re


def create_drivers(driverdict=None):
    if not driverdict:
        driverdict = {}

    raw = pd.read_clipboard()
    for index, data in raw.iterrows():
        splitname = data['Name'].split(' ')
        if len(splitname) <= 2:
            name3 = splitname[1][0:3]
            name3 = name3.upper()
        print(index)

        driverobj = f1classes.driver(data['Name'], data['Team'], name3)
        driverdict[name3] = driverobj
    return(driverdict)


def data_creation():
    # raw = pd.read_clipboard()
    pass


if __name__ == "__main__":
    driverdict = create_drivers()
