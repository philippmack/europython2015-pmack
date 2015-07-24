import pandas as pd
import numpy as np
from replenishment_rules import *
from prediction.predict import *
import sys

def order(df, config):

   prediction = config['replenishment']['prediction']['model']
   prediction_func = eval(prediction)

   replenishment_rule=config['replenishment']['replenishment']['model']
   replenishment_rule_func = eval(replenishment_rule)
   quantile =  config['replenishment']['quantiles']

   '''
   do predictions and replenishment
   '''
   prediction_window= config['replenishment']['prediction']['window']
   prediction_func(df,'PRODUCT_ID',prediction_window, 0)

   df['ORDER'] = df['PREDICTION'].apply(lambda x : replenishment_rule_func(0,0,quantile,x))

   return df
