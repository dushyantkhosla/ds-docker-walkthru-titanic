from src.scrub import compress_numeric, compress_categorical
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

df = DataFrame({
    'strs': np.random.choice(['BLR', 'DEL', 'BRU', 'CDG', 'AMS', 'GVA', 'KRK'], size=10**5, replace=True),
    'ints': np.random.randint(-100, 100, 10**5),
    'floats': np.random.randn(10**5),
    'categ': pd.Categorical(np.random.choice(['HIGH', 'MEDIUM', 'LOW'], size=10**5, replace=True))
    })

df.info()

df.dtypes

df.head()

df.select_dtypes(include=np.numeric, exclude=None)
