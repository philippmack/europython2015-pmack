import pandas as pd
import numpy as np
from multiprocessing import Pool
import simulation.simulation as sim
import sys


if __name__ == "__main__":

   #read in config

   version_id =sys.argv[1]
   liste = np.arange(10,100,10)

   pool = Pool(processes=4)
   result = pool.map(sim.simulate_per_quantile,liste)
   print result

   dfxy = pd.DataFrame( result, columns=['SURPLUS', 'OOS', 'QUANTILE'])
   dfxy['VERSION_ID']=version_id
   dfxy.to_csv('test_result%s.csv' %version_id,sep=';')

