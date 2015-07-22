import pandas as pd
import numpy as np
from replenishment_rules import *
from prediction.predict import *
import sys

def order(arguments_partial):

   df = pd.read_csv('temp.csv',sep=';')
   df = df[df['DATE']<='2015-03-01']
   df = df.sort(['PRODUCT_ID','DATE'])
   df = df.reset_index()

   prediction = arguments_partial['simulation']['prediction']['model']
   prediction_func = eval(prediction)
   prediction_func(df,'PRODUCT_ID',5, 0)

   replenishment_rule=arguments_partial['simulation']['replenishment']['model']
   replenishment_rule_func = eval(replenishment_rule)

   quantile = 50

   df['ORDER'] = df['PREDICTION'].apply(lambda x : replenishment_rule_func(0,0,quantile,x))

   df = df.dropna()

   return df
