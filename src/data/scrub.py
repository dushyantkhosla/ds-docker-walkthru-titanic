import os
import pandas as pd

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
    
    # fix column names
    df.columns = \
    (pd.Series(df.columns)
     .map(lambda i: i.lower().translate(None, './()& '))
    )
    
    # rename columns
    df.rename(columns={'siblingsspousesaboard': 'sibsp'}, inplace=True)
    
    # missing data flags
    df['age__is_null'] = df['age'].isnull().map(int)
    df['cabinnumber__is_null'] = df['cabinnumber'].isnull().map(int)
    
    # impute missings
    df['age'].fillna(value=df['age'].median(), inplace=True)
    
    # create gender column
    df.loc[:, 'gender'] = df['name'].map(lambda i: 1 if 'Miss' in i or 'Mrs' in i else 0)
    
    # create dummies
    df = df.join(pd.get_dummies(df['embarked'], prefix='embarked'))
    df = df.join(pd.get_dummies(df['passengerclass'], prefix='pclass'))
    
    # drop columns
    df.drop(['cabinnumber', 'ticket', 'name', 'embarked', 'passengerclass'], axis=1, inplace=True)
    
    # convert to numeric types
    df = df.apply(lambda c: pd.to_numeric(c, downcast='integer'))
    
    # backup
    df.to_csv("/home/data/04-processed/titanic.csv", index=False)
    
    return df
    