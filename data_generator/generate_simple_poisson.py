__author__ = 'pmack'

import pandas as pd
import numpy as np
from scipy.stats import poisson

def generate_data():
    product = np.arange(100)
    date_rng = pd.date_range('2014-01-01','2015-06-01',freq='D')
    product_rand = np.random.randint(1,10,100)

    df = pd.DataFrame(columns=['PRODUCT_ID','DATE','SALES'])

    temp_df= []

    for i,p in enumerate(product) :
        sales_mean = product_rand[i]
        sales = np.random.poisson(sales_mean,len(date_rng))
        temp_df.append(pd.DataFrame({'PRODUCT_ID' : i, 'DATE' : date_rng, 'SALES' : sales}))


    df = pd.concat(temp_df)
    return df

dfr = generate_data()
dfr.to_csv('temp.csv',sep=';')
