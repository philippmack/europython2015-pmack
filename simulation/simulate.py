from numpy import random
from scipy.stats import poisson, skellam
import pandas as pd
import numpy as np
import logging
import traceback


def stochastic_round(value) :
    """
        This rounds a float stochastically to an integer.
    """
    return int(round(value + random.uniform(-0.5, 0.5)))

def replenishment(stock,open_orders,quantile,sales_prog):
    sales_quant = poisson.ppf(quantile/100.,sales_prog+1.E-3)
    order = max(0,(sales_quant) - (stock + open_orders))
    return stochastic_round(order)

def stock_simulation_rule(stock_yesterday,sales,incoming):
    stock = stock_yesterday + incoming
    stock_virtual = max(0,stock - min(stock,sales))
    missing = max(0, sales - stock)
    surplus =max(0, stock-sales)
    return stock_virtual, missing, surplus

def simulate(dataframe, obligo_horizon,quantile,array_result):


  logger = logging.getLogger(__name__)

  start_lib = 0
  loop_aktueller_lib = 0
  reste=0
  first_index_of_new_article = -999

  # Loop ueber ITEMOPTION_COMKEYS

  for i, (index, row) in enumerate(dataframe.iterrows()):

    if i == 0 : 
        first_index_of_new_article = index

    # Bestandssimulation fuer diesen Tag
    if i > 0 :

        # Vortagesbestand, bezogen auf diesen Tag,
        # wird bestimmt ueber Loopvariable
        lib_vortag = 0

        # Berechne Wareneingang fuer diesen Tag
        wareneingang = 0
        wareneingang_indices = np.arange(index-obligo_horizon,index-obligo_horizon+1)
        wareneingang_indices = wareneingang_indices[np.where((wareneingang_indices>=0) & (wareneingang_indices>=first_index_of_new_article))]
        for wareneingang_index in wareneingang_indices :
            wareneingang += array_result[wareneingang_index, 0]

        # Stock Simulation
        (aktueller_lib,sim_ova,reste) = stock_simulation_rule(
            lib_vortag,
            int(row['ANSPR_MG']),
            wareneingang)

    # Spezialfall erster Tag
    else :
        aktueller_lib = 0
        sim_ova=0
    obligo = 0
    
    # Replenishment
    anspr_mg_prog = int(row['PROG_MG'])
    bestellmenge = replenishment(aktueller_lib,obligo,quantile,anspr_mg_prog) 

    # Aktualisierung der Schleifenvariable
    loop_aktueller_lib = aktueller_lib

    # Abspeichern der Ergebnisse im Result-Array
    array_result[index, 0] = bestellmenge
    array_result[index, 1] = reste
    array_result[index, 2] = sim_ova

def loop(dataframe,obligo_horizon,quantile):
     
     # Create NUMPY arrays to hold evaluation result
     df_len = len(dataframe)
     array_result = np.zeros(shape=(df_len, 3), dtype=int)

     for i, (itemoption_comkey, dataframe_group) in  enumerate(dataframe.groupby(['ITEMOPTION_COMKEY'])):
          if i%100==0 :print i
          simulate(dataframe_group, obligo_horizon,quantile,array_result)
   
     return array_result


def rename(dataframe):
    dataframe = dataframe.rename(columns={'PRODUCT_ID' : 'ITEMOPTION_COMKEY' ,    'SALES' :'ANSPR_MG'})
    return dataframe


def first(quantile):
   df = pd.read_csv('temp.csv',sep=';')
   df = rename(df)
   df = df.sort(['ITEMOPTION_COMKEY','DATE'])
   df = df.reset_index()
   df['PROG_MG'] = df.groupby(['ITEMOPTION_COMKEY'])['ANSPR_MG'].transform(lambda x : x) 

   from IPython import embed
   embed()
   result = loop(df,1,quantile)

   df['BESTELLVORS'] = 0 
   df['SIM_LIB_MG'] = 0
   df['SIM_OVA_MG'] = 0

   df_result = pd.DataFrame(
        result,
        columns=[
            'BESTELLVORS',
            'SIM_LIB_MG',
            'SIM_OVA_MG'
        ]
       )

   df.update(df_result)

   #df.to_csv('test_result.csv',sep=';')

   print 
   print 'abschrift : ', df['ANSPR_MG'].sum(),float(df.SIM_LIB_MG.sum())
   print 'oos : ', len(df[df['SIM_OVA_MG']>0]),float(len(df))
   abschrift =  float(df.SIM_LIB_MG.sum())/df['ANSPR_MG'].sum()

   return abschrift,len(df[df['SIM_OVA_MG']>0])/float(len(df))



from multiprocessing import Pool


x=[]
y=[]
q=[]


liste = [10,20,30,40,50,60,70,80,90]
pool = Pool(processes=4)
result = pool.map(first,liste)

print result
#first(10)

#    a,b = first(I)
#    x.append(b)
#    y.append(a)
#    q.append(I)

#print x,y,q

#dfxy = pd.DataFrame( { 'OOS' : x , 'ABS' : y , 'QUANTILE' : q} )

#dfxy.to_csv('test_result.csv',sep=';')

