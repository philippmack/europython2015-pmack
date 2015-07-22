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

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument("-y","--yaml", help="yaml inputfile to test", type=str)

   args = parser.parse_args()

   # parse config file
   sim_args = parse_yaml(args.yaml)


   start_time = time.time()

   order_df = rep.order(sim_args)

   end_time = time.time()

   print "--- %s seconds ---" % (end_time - start_time)

   order_df.to_csv('order.csv',sep=';')

