__author__ = 'pmack'

import replenishment.replenishment_rules as rp
import replenishment.replenishment as ord
import pandas as pd
import pandas.util.testing as pdt
import numpy.testing as npt
import numpy as np


def test_order_one_replenishment():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011', periods=5, freq='D'), 'PREDICTION' : [2,3,4,5,6]})
    quantile = 10
    df['ORDER'] = df['PREDICTION'].apply(lambda x : rp.order_one_replenishment(0,0,quantile,x))
    npt.assert_array_equal(df['ORDER'], [1]*5)

def test_order_ten_replenishment():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011', periods=5, freq='D'), 'PREDICTION' : [2,3,4,5,6]})
    quantile = 10
    df['ORDER'] = df['PREDICTION'].apply(lambda x : rp.order_ten_replenishment(0,0,quantile,x))
    npt.assert_array_equal(df['ORDER'], [10]*5)


def test_order_expectation_replenishment():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011',periods=5, freq='D'), 'PREDICTION' : [2,3,4,5,6]})
    quantile = 10
    df['ORDER'] = df['PREDICTION'].apply(lambda x : rp.order_expectation_replenishment(0,0,quantile,x))
    npt.assert_array_equal(df['ORDER'], [2,3,4,5,6])

def test_replenishment():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011',periods=5, freq='D'), 'PREDICTION' : [2,3,4,5,6]})
    quantile = 70
    df['ORDER'] = df['PREDICTION'].apply(lambda x : rp.replenishment(0,0,quantile,x))
    npt.assert_array_equal(df['ORDER'], [3,4,5,6,7])

def test_order():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011',periods=5, freq='D'), 'SALES' : [2,3,4,1,1],
                        })
    config = {'replenishment': {'quantiles': 70, 'replenishment': {'model': 'replenishment'},
                                'prediction': {'model': 'simple_prediction', 'window': 0}, 'input_file': 'temp.csv'}}
    result = ord.order(df,config)
    npt.assert_array_equal(df['ORDER'], [3,4,5,1,1])

