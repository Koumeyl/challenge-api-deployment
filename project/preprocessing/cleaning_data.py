from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pandas import json_normalize
import numpy as np
import pandas as pd
def preprocessing(df):
    df['building_state'] = (df['building_state']).replace({'GOOD': 0, 'NEW': 1, 'TO RENOVATE': 0, 
    'JUST RENOVATED': 0, 'TO REBUILD':0})
    u = df.select_dtypes(bool)
    df[u.columns] = u.astype(int)
    df.head()
    return df
