import pandas as pd
import numpy as np
from multiprocessing import Pool
import simulation.simulation as sim
import sys
from config.yaml_parser import *
from config.validator import *
import itertools
import argparse
import time
import datetime

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument("-y","--yaml", help="yaml config", type=str)
   parser.add_argument("-v","--version", help="version_id", type=str)

   args = parser.parse_args()

   # parse config file
   sim_args = parse_yaml(args.yaml)
   startdate = datetime.datetime.strptime(sim_args['simulation']['startdate'],'%Y-%m-%d')
   enddate = datetime.datetime.strptime(sim_args['simulation']['enddate'],'%Y-%m-%d')
   df = pd.read_csv(sim_args['simulation']['input_file'] ,sep=';',parse_dates=['DATE'])
   df = df[ (df['DATE']>=startdate) & (df['DATE']<=enddate)]
   df = df.sort(['PRODUCT_ID','DATE'])
   df = df.reset_index()
   sim_args['simulation_df'] = df

   liste = sim_args['simulation']['quantiles']
   list_args = itertools.izip(liste, itertools.repeat(sim_args))

   start_time = time.time()

   pool = Pool(processes=4)
   result = pool.map(sim.simulate_wrapper,list_args)

   end_time = time.time()

   print "--- %s seconds ---" % (end_time - start_time)

   dfxy = pd.DataFrame( result, columns=['SURPLUS', 'OOS', 'QUANTILE'])
   dfxy['VERSION_ID']=args.version
   dfxy.to_csv('test_result%s.csv' %args.version,sep=';')

