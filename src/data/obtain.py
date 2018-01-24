import os
import json
import pandas as pd

# Declare constants
ROOT = '/home'
PATH_TO_DATA_RAW = ROOT + 'data/00-raw/'

URL_TITANIC = 'https://raw.githubusercontent.com/dushyantkhosla/tiny-datasets/master/titanic.csv'

# Declare functions
def get_raw_data(filename='titanic_data.csv', url=URL_TITANIC, force_download=False):
    """Download and cache the Titanic Data
    
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
    import pandas as pd
    if force_download or not os.path.exists(PATH_TO_DATA_RAW + filename):
        df_raw = pd.read_csv(URL_TITANIC)
    else:
        df_raw = pd.read_csv(PATH_TO_DATA_RAW + filename)
        
    return df_raw
        
        
def json_read(f):
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
        if os.path.exists(f):
            with open(f, 'r') as fp:
                return json.load(fp)
        else:
            print("File does not exist.")
    except:
        print("An error occured while reading the JSON file.")
        
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