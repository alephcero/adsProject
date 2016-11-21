import pandas as pd
import numpy as np

def categorize(df):
    df.female = (df.female == 2).astype(int)
    df.schoolLevel.replace(to_replace=[99], value=[np.nan] , inplace=True, axis=None) 
    df.lastYear.replace(to_replace=[98,99], value=[np.nan, np.nan] , inplace=True, axis=None)
    df.activity.replace(to_replace=[0], value=[np.nan] , inplace=True, axis=None)
    df.empCond.replace(to_replace=[0], value=[np.nan] , inplace=True, axis=None)
    df.unempCond.replace(to_replace=[0], value=[np.nan] , inplace=True, axis=None)
    return df

