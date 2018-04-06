import os
import json
import string
import pandas as pd
from pandas import Series, DataFrame

from src import URL_TITANIC
from src.obtain import get_raw_data

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
    # === PERSIST ===
    print("Declaring an empty dictionary to persist information we'll need to scrub new data in production.")
    dict_persist = {}

    # === COLNAMES ===

    remove_ = str.maketrans(dict.fromkeys(string.punctuation + ' '))

    print("Fixing column names. (Removing special characters, converting to lowercase. Renaming long columns)")
    df.columns = list(map(lambda i: i.lower().translate(remove_), df.columns.tolist()))
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

    dict_persist['have_missing'] = have_missing

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

    dict_persist['age_fillna'] = age_fillna
    dict_persist['fare_fillna'] = fare_fillna
    dict_persist['embarked_fillna'] = embarked_fillna

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

    print("Backing up the data/")
    df.to_csv("data/04-processed/titanic.csv", index=False)

    with open("data/02-interim/scrub_params.json", 'w') as fp:
        json.dump(dict_persist, fp)
    print("Scrub Parameters have been presisted at 'data/interim/scrub_params.json'")
    print("Okay, all Done. Happy Exploring!")

    return df

def get_clean_data():
    """
    Recover cleaned data from backup or download again and clean it
    """
    if not os.path.exists("data/04-processed/titanic.csv"):
        df_titanic_clean = scrub_raw_data(get_raw_data(url=URL_TITANIC))
        df_titanic_clean.to_csv("data/processed/titanic.csv", index=False)
    else:
        df_titanic_clean = pd.read_csv("data/04-processed/titanic.csv")
    return df_titanic_clean

if __name__ == '__main__':
    import sys
    sys.path.append(os.getcwd())
    from src import URL_TITANIC
    df_titanic = get_raw_data(url=URL_TITANIC)
    df = get_clean_data()
