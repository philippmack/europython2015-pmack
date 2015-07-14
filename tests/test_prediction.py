__author__ = 'pmack'

import prediction.predict as pr
import pandas as pd
import pandas.util.testing as pdt
import numpy.testing as npt
import numpy as np

def test_prediction_simple():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011', periods=5, freq='D'), 'SALES' : [2,3,4,5,6]})
    result = pr.simple_prediction(df,'PRODUCT_ID',1)
    npt.assert_array_equal(result['PREDICTION'], [np.nan,2,3,4,5])

def test_prediction_rmean():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011', periods=6, freq='D'), 'SALES' : [2,1,2,1,4,1]})
    result = pr.rmean_prediction(df,'PRODUCT_ID',5,1)
    npt.assert_array_equal(result['PREDICTION'], [np.nan]*5 + [2.0])

