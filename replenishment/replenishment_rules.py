from scipy.stats import poisson, skellam
import pandas as pd
import numpy as np
import logging


def stochastic_round(value) :
    """
        This rounds a float stochastically to an integer.
    """
    return int(round(value + np.random.uniform(-0.5, 0.5)))

### simple rule
def order_one_replenishment(stock,open_orders,quantile,sales_prog):
    return 1.0

def order_ten_replenishment(stock,open_orders,quantile,sales_prog):
    return 10.0

### order expectation value
def order_expectation_replenishment(stock,open_orders,quantile,sales_prog):
    order = max(0,(sales_prog) - (stock + open_orders))
    return stochastic_round(order)

### general rule
### order = predicted demand - ( expected stock + open_order)
def replenishment(stock,open_orders,quantile,sales_prog):
    '''

    :param stock: stock
    :param open_orders: open incoming orders
    :param quantile: chosen quantile
    :param sales_prog: forecast for demand
    :return: order
    '''
    sales_quant = poisson.ppf(quantile/100.,sales_prog+1.E-3)
    order = max(0,(sales_quant) - (stock + open_orders))
    return stochastic_round(order)

