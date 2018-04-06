import numpy  as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def compress_numeric(COL):
    """
    If the passed COL is numeric,
    downcast it to the lowest size.
    Else,
    Return as-is.

    Parameters
    -----------
    COL: pandas.Series
        The Series to shrink

    Returns
    -------
    if numeric, a compressed series
    """
    if 'float' in str(COL.dtype):
        print("Downcasting {} to float".format(COL.name))
        result = pd.to_numeric(COL, downcast='float', errors='ignore')
    elif 'int' in str(COL.dtype):
        print("Downcasting {} to int".format(COL.name))
        result = pd.to_numeric(COL, downcast='integer', errors='ignore')
    else:
        print("{} is not numeric. Returning as-is".format(COL.name))
        result = COL
    return result

def compress_categorical(COL):
    """
    """
    from src.scrub import clip_categorical
    le = LabelEncoder()
    COL_clipped = clip_categorical(COL, MIN_LEVELS=8)
    le.fit(COL_clipped)

    lookup = {k:v for k,v in enumerate(le.classes_)}
    path_persist = "data/interim/{}_lookup.json".format(COL.name)
    with open(path_persist, 'w') as fp:
        json.dump(lookup, fp)

    return pd.Series(le.transform(COL_clipped), index=COL.index, name=COL.name)
