__author__ = 'pmack'

import prediction.predict as pr
import pandas as pd
import pandas.util.testing as pdt
import numpy.testing as npt
import numpy as np

def test_prediction():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011', periods=5, freq='D'), 'SALES' : [2,3,4,5,6]})
    result = pr.simple_prediction(df,'PRODUCT_ID')
    npt.assert_array_equal(result['PREDICTION'], [np.nan,2,3,4,5])
