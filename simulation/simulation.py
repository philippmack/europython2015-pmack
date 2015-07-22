import pandas as pd
import numpy as np
from replenishment.replenishment_rules import *
from stock_simulation import *
from prediction.predict import * 
import sys

def simulate_wrapper(arguments):
   return simulate_per_quantile(*arguments)

def simulate_per_quantile(quantile, arguments_partial):

   '''
   simulation interface
:param quantile: quantile of distribution
:return: excess and out of stock rate
'''

   df = pd.read_csv('temp.csv',sep=';')
   df = df.sort(['PRODUCT_ID','DATE'])
   df = df.reset_index()

   prediction = arguments_partial['simulation']['prediction']['model']
   prediction_func = eval(prediction)
   prediction_func(df,'PRODUCT_ID',5, 0)

   replenishment_rule=arguments_partial['simulation']['replenishment']['model']
   replenishment_rule_func = eval(replenishment_rule)

   df['ORDER'] = df['PREDICTION'].apply(lambda x : replenishment_rule_func(0,0,quantile,x))
   df['INCOMING'] = df.groupby('PRODUCT_ID')['ORDER'].transform(lambda x :  x.shift(1) )
   df['STOCK_YESTERDAY'] = 0.0
  
   df_temp = pd.DataFrame( map(stock_simulation_rule,df['STOCK_YESTERDAY'], df['SALES'], df['INCOMING']), columns = ['STOCK', 'missing', 'surplus'])
   
   df['surplus']= df_temp['surplus']
   df['missing']= df_temp['missing']

   df = df.dropna()

   surplus =  float(df.surplus.sum())/df['SALES'].sum()
   oos_quota = len(df[df.missing>0])/float(len(df))

   return surplus,oos_quota,quantile
