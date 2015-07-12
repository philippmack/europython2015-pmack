import pandas as pd
import numpy as np

def simple_prediction(df, groupkey):
     
    df['PREDICTION'] = df.groupby('PRODUCT_ID')['SALES'].transform( lambda x : x.shift(1) )
    
    return df

def rmean_prediction(df, groupkey, window):

    df['PREDICTION'] = df.groupby('PRODUCT_ID')['SALES'].transform( lambda x : pd.rolling_mean(x,window=window).shift(1) )

    return df
