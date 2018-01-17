import os
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
        
        
        