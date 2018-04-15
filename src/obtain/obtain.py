import os
import json
import pandas as pd

def get_raw_data(url, force_download=False):
    """
    Download and cache the Titanic Data

    Parameters
    ----------
    filename: string (optional)
        location to save the data
    url: string (optional)
        web location of the data
    force_download: bool (optional)
        if True, download the data again

    Returns
    -------
    df_raw: pandas.DataFrame
        The Titanic data
    """
    if force_download or not os.path.exists("data/00-raw/titanic.csv"):
        print("Downloading data...")
        df_raw = pd.read_csv(url)
        df_raw.to_csv("data/00-raw/titanic.csv", index=False)
    else:
        print("Retrieving data from backup...")
        df_raw = pd.read_csv("data/00-raw/titanic.csv")
    return df_raw


def json_read(file):
    """
    Read a JSON file into a Python Dict

    Parameters
    ----------
    f: string
        Path to a .json file

    Returns
    -------
    Dictionary
    """
    try:
        if os.path.exists(file):
            with open(file, 'r') as fp:
                return json.load(fp)
        else:
            print("File does not exist.")
            return None
    except:
        print("An error occured while reading the JSON file.")
        return None

def json_write(x, path):
    """
    Write a python dict to a JSON file

    Parameters
    ----------
    x: dict
        The object to be persisted
    path: string
        The file to be written to.
    """
    with open(path, 'w') as fp:
        json.dump(x, fp)

    return None

if __name__ == '__main__':
    import sys
    sys.path.append(os.getcwd())
    from src import URL_TITANIC
    df_titanic = get_raw_data(url=URL_TITANIC)
