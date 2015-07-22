import pandas as pd
import numpy as np

def simple_prediction(df, groupkey, window, shift_value):
     
    df['PREDICTION'] = df.groupby(groupkey)['SALES'].transform( lambda x :  x.shift(shift_value) )
    
    return df

def rmean_prediction(df, groupkey, window, shift_value):

    df['PREDICTION'] = df.groupby(groupkey)['SALES'].transform( lambda x :  pd.rolling_mean(x,window=window).shift(shift_value) )

    return df

def ewma_prediction(df, groupkey, window, shift_value):

    df['PREDICTION'] = df.groupby(groupkey)['SALES'].transform( lambda x :  pd.ewma(x,span=window).shift(shift_value) )

    return df



