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
    
    # Scrub
    df.columns = map(lambda i: i.lower().translate(None, './()& '), 
                     df.columns.tolist())
    df.rename(columns={'siblingsspousesaboard': 'sibsp'}, inplace=True)
    
    
    have_missing = 
    
    for COL in have_missing:
    """
    Create a missing flag for each column
    that has missing data.
    """
    newCOL = COL + '__is_null'
    df.loc[:, newCOL] = df.loc[:, COL].isnull().astype(int)
    
    
    # Preprocess
    
    
    # Model
   
    