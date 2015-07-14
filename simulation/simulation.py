import pandas as pd
import numpy as np
import logging
import traceback
from multiprocessing import Pool
from replenishment.replenishment_rules import order_expectation_replenishment, replenishment 
from stock_simulation import *
from prediction.predict import * 
import sys

def simulate_per_quantile(quantile):

   df = pd.read_csv('temp.csv',sep=';')
   df = df.sort(['PRODUCT_ID','DATE'])
   df = df.reset_index()

   prediction = "rmean_prediction"
   prediction_func = eval(prediction)
   prediction_func(df,'PRODUCT_ID',5, 0)

   replenishment_rule="replenishment"
   replenishment_rule_func = eval(replenishment_rule)

   df['ORDER'] = df['PREDICTION'].apply(lambda x : replenishment_rule_func(0,0,quantile,x))
   df['INCOMING'] = df.groupby('PRODUCT_ID')['ORDER'].transform(lambda x :  x.shift(1) )
   df['STOCK_YESTERDAY'] = 0.0
  
   df_temp = pd.DataFrame( map(stock_simulation_rule,df['STOCK_YESTERDAY'], df['SALES'], df['INCOMING']), columns = ['STOCK', 'missing', 'surplus'])
   
   df['SIM_LIB_MG']= df_temp['surplus']
   df['SIM_OVA_MG']= df_temp['missing']

   df = df.dropna()
   abschrift =  float(df.SIM_LIB_MG.sum())/df['SALES'].sum()

   df.to_csv('temp_%s.csv' %quantile, sep=';')

   return abschrift,len(df[df['SIM_OVA_MG']>0])/float(len(df)),quantile

if __name__ == "__main__":

   #read in config

   version_id =sys.argv[1]
   liste = np.arange(10,100,10)

   pool = Pool(processes=4)
   result = pool.map(simulate_per_quantile,liste)
   print result

   dfxy = pd.DataFrame( result, columns=['SURPLUS', 'OOS', 'QUANTILE'])
   dfxy['VERSION_ID']=version_id
   dfxy.to_csv('test_result%s.csv' %version_id,sep=';')
