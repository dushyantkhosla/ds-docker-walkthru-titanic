import os
os.chdir("/home")

import pandas as pd
from pandas import Series, DataFrame

def json_save(x, PATH):
    """
    Save a Python Dict as a JSON file for persistence
    
    Parameters
    ----------
    x: dict
        The Python dict to be persisted
    PATH: string
        The full path to destination folder
        
    Returns
    -------
    None
    """
    import json
    with open(PATH, 'w') as fp:
        json.dump(x, fp, sort_keys=True, indent=4)
    
    return None

def scrub_raw_data(df):
    """
    Fix column names
    Rename columns
    Create flags for missing data, outliers
    Impute missings
    Clip outliers
    Create derived features
    Create dummies for categorical
    Drop columns with no predictive power
    
    Parameters
    ----------
    df: pandas.DataFrame
        The raw Titanic data
        
    Returns
    -------
    df_clean: pandas.DataFrame
        The cleaned Titanic data
    """
    # === COLNAMES ===
    
    print("Fixing column names. (Removing special characters, converting to lowercase. Renaming long columns)")
    df.columns = map(lambda i: i.lower().translate(None, './()& '), 
                     df.columns.tolist())

    df.rename(columns={'siblingsspousesaboard': 'sibsp'}, inplace=True)   
    
    # === MISSINGS ===
    
    have_missing = \
    (df
     .isnull()
     .sum()
     .where(lambda x: x > 0)
     .dropna()
     .index
     .tolist()
    )

    print("The following columns have missing data: \n{}".format(have_missing))
    
    for COL in have_missing:
    """
    Create a missing flag for each column
    that has missing data.
    """
    newCOL = COL + '__is_null'
    df.loc[:, newCOL] = df.loc[:, COL].isnull().astype(int)
    
    print("Age is approximately normally distributed, but Fare is skewed.")
    print("Using the mean for Age and Median for Fare to impute missing data.")
    print("Cabin Number has over 70% values missing. Dropping this variable.")
    print("Embarked has only 2 values missing. Imputing with Mode.")

    age_fillna = df['age'].mean()
    fare_fillna = df['fare'].median()
    embarked_fillna = df['embarked'].describe()['top']

    df['age'].fillna(value=age_fillna, inplace=True)
    df['fare'].fillna(value=fare_fillna, inplace=True)
    df['embarked'].fillna(value=embarked_fillna, inplace=True)
    
    # === NEW FEATURES, DUMMIES ===
    
    print("Creating a column for Gender")
    df.loc[:, 'gender'] = df['name'].map(lambda i: 1 if 'Miss' in i or 'Mrs' in i else 0)
    
    print("Creating Dummies for Embarked and Passenger Class. \nDone. Now dropping these.")

    df = df.join(pd.get_dummies(df['embarked'], prefix='embarked'))
    df = df.join(pd.get_dummies(df['passengerclass'], prefix='pclass'))

    df.drop(['embarked', 'passengerclass'], axis=1, inplace=True)
    
    # === DROP ===
    
    print("Dropping cabinnumber, ticket and name as they have no predictive value. (Too many uniques)")
    df.drop(['cabinnumber', 'ticket', 'name'], axis=1, inplace=True)
    
    # === TO NUMERIC ===
    
    print("Downcasting numerics to occupy less space.")
    df = df.apply(lambda c: pd.to_numeric(c, downcast='integer'))
    
    # === BACKUP ===
    
    print("Backing up the data. \nOkay, all Done. Happy Exploring!")
    df.to_csv("/home/data/04-processed/titanic.csv", index=False)
    
    return df
    
