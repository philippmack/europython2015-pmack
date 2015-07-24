__author__ = 'pmack'

import simulation.stock_simulation as st
import pandas as pd
import pandas.util.testing as pdt
import numpy.testing as npt
import numpy as np

def test_stock_simulation():
    result = st.stock_simulation_rule(0,5,3)
    npt.assert_array_equal(result, [0,2,0])
