import pandas as pd
import numpy as np
from multiprocessing import Pool
import replenishment.replenishment as rep
import sys
from config.yaml_parser import *
from config.validator import *
import itertools
import argparse
import time
import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yaml", help="yaml inputfile to test", type=str)
    parser.add_argument("-d", "--orderday", help="date of order", type=str)
    args = parser.parse_args()

    # parse config file
    rep_args = parse_yaml(args.yaml)
    test_file(rep_args, 'replenishment')

    start_time = time.time()
    '''
    read in file
    '''
    df = pd.read_csv(rep_args['replenishment']['input_file'],sep=';', parse_dates=['DATE'])
    orderday = datetime.datetime.strptime(args.orderday,'%Y-%m-%d')
    df = df[df['DATE']<=orderday]
    df = df.sort(['PRODUCT_ID','DATE'])
    df = df.reset_index()

    order_df = rep.order(df,rep_args)
    order_df = order_df[order_df['DATE']==orderday]

    end_time = time.time()

    print "--- %s seconds ---" % (end_time - start_time)

    order_df.to_csv('order.csv', sep=';')
