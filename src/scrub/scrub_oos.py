import os
import json   
import pandas as pd
from src import scrub_params

os.chdir("/home")

def scrub_oos_data(df):
    """
    Apply the same set of transformations to the OOS data
    as was applied to the training set.
    
    This is critical to ensure 
    that the model can run on the new data.
    
    Parameters
    ----------
    df: pandas.DataFrame
        The incoming data
        
    Returns
    -------
    df: pandas.DataFrame
        Prepared data, ready to be consumed by the model
    """
    
    # === COLLECT THINGS ===
    with open(scrub_params, 'r') as fp:
        dict_persist = json.load(fp)
    
    have_missing = dict_persist['have_missing']
    age_fillna = dict_persist['age_fillna']
    fare_fillna = dict_persist['fare_fillna'] 
    embarked_fillna = dict_persist['embarked_fillna']
   
    # === Scrub ===
    df.columns = map(lambda i: i.lower().translate(None, './()& '), 
                     df.columns.tolist())
    df.rename(columns={'siblingsspousesaboard': 'sibsp'}, inplace=True)
    
    for COL in have_missing:
        """
        Create a missing flag for each column
        that has missing data.
        """
        newCOL = COL + '__is_null'
        df.loc[:, newCOL] = df.loc[:, COL].isnull().astype(int)
       
    df['age'].fillna(value=age_fillna, inplace=True)
    df['fare'].fillna(value=fare_fillna, inplace=True)
    df['embarked'].fillna(value=embarked_fillna, inplace=True)
    
    df.loc[:, 'gender'] = \
    df['name'].map(lambda i: 1 if 'Miss' in i or 'Mrs' in i else 0)
    
    df = df.join(pd.get_dummies(df['embarked'], prefix='embarked'))
    df = df.join(pd.get_dummies(df['passengerclass'], prefix='pclass'))

    df.drop(['embarked', 'passengerclass'], axis=1, inplace=True)
    df.drop(['cabinnumber', 'ticket', 'name'], axis=1, inplace=True)
    
    if 'survived' in df.columns:
        df.drop(['survived'], axis=1, inplace=True)
    
    df = df.apply(lambda c: pd.to_numeric(c, downcast='integer'))
    
    return df

    # Preprocess
    
    
    # Model
   
    