import pickle
import pandas as pd
import f1classes
import re


def create_drivers(driverdict=None):
    if not driverdict:
        driverdict = {}

    raw = pd.read_clipboard()
    for data in raw.iterrows():
        splitname = data['Name'].split(' ')
        if len(splitname) <= 2:
            name3 = splitname[1][0:4]

        driverobj = f1classes.driver(data['Name'], data['Team'], name3)
        driverdict[name3] = driverobj


def data_creation():
    # raw = pd.read_clipboard()
    pass


if __name__ == "__main__":
    print("helloworld")
