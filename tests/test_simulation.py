__author__ = 'pmack'

import simulation.stock_simulation as st
import simulation.simulation as sim
import pandas as pd
import pandas.util.testing as pdt
import numpy.testing as npt
import numpy as np

def test_stock_simulation():
    result = st.stock_simulation_rule(0,5,3)
    npt.assert_array_equal(result, [0,2,0])

def test_simulation():
    df = pd.DataFrame( { 'PRODUCT_ID' : 1 , 'DATE' : pd.date_range('1/1/2011',periods=5, freq='D'), 'SALES' : [2,3,4,1,1],
                        })
    config = {'simulation': {'quantiles': 70, 'replenishment': {'model': 'replenishment'},
                                'prediction': {'model': 'simple_prediction', 'window': 0}, 'input_file': 'temp.csv'}}
    config['simulation_df'] = df
    result = sim.simulate_per_quantile(70,config)
    npt.assert_array_almost_equal(result, [0.444444,0,70])