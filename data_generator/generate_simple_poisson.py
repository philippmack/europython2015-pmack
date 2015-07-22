__author__ = 'pmack'

import argparse
import pandas as pd
import numpy as np
from scipy.stats import poisson


def generate_data(number_of_products,start,end):
    '''

    :param number_of_products: number of items to generate
    :param start: start date
    :param end: end date
    :return: dataframe with timeseries of poisson distributed sales per product
    '''
    product = np.arange(number_of_products)
    date_rng = pd.date_range(start,end,freq='D')
    product_rand_sales = np.random.randint(1,10,100)

    df = pd.DataFrame(columns=['PRODUCT_ID','DATE','SALES'])

    temp_df= []

    '''
    loop over products, not fast but for this simple example OK
    '''
    for i,p in enumerate(product) :
        sales_mean = product_rand_sales[i]
        sales = np.random.poisson(sales_mean,len(date_rng))
        temp_df.append(pd.DataFrame({'PRODUCT_ID' : i, 'DATE' : date_rng, 'SALES' : sales}))

    df = pd.concat(temp_df)
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--outputfile", help="outputfilename", type=str)
    parser.add_argument("-n","--number", help="number_of_products", type=int)
    parser.add_argument("-s","--startdate", help="start date", type=str)
    parser.add_argument("-e","--enddate", help="end date", type=str)

    args = parser.parse_args()

    dfr = generate_data(args.number,args.startdate,args.enddate)
    dfr.to_csv(args.outputfile,sep=';')
