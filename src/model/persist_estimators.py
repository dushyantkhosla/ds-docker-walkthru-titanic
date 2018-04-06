import numpy as np
from src.obtain import json_read, json_write

def persist(e):
    """
    Convert a sklearn estimator into a JSON object for persistence
    
    Parameters
    ----------
    e: Estimator
        An sklearn estimator
        
    Returns
    -------
    persist: dict
        A dictionary containing a copy of the data in 'e'
        in JSON friendly formats
    """
    d = {}
    for k,v in e.__dict__.items():
        d[k] = v.tolist() if isinstance(v, np.ndarray) else v
        
    return d


def recover(path='', estimator=''):
    """
    Build Estimator from JSON
    
    Parameters
    ----------
    path: string
        Location of the JSON file
        
    Returns
    -------
    est: sklearn Estimator
        The sklearn estimator with attributes updated
    """
    recovered_params = {}
    
    for k, v in json_read(path).items():
        if k[-1] == "_":
            recovered_params[k] = np.array(v)
        else:
            recovered_params[k] = v

    for item in recovered_params.items():
        k, v = item[0], item[1]
        setattr(estimator, k, v)
        
    return estimator