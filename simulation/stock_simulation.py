__author__ = 'pmack'

def stock_simulation_rule(stock_yesterday,sales,incoming):
    '''

    :param stock_yesterday: last known stock amount
    :param sales: simulated sales (truth)
    :param incoming: incoming goods
    :return: virtual stocks, missing and surplus in the evening
    '''
    stock = stock_yesterday + incoming
    stock_virtual = max(0,stock - min(stock,sales))
    missing = max(0, sales - stock)
    surplus =max(0, stock-sales)
    return stock_virtual, missing, surplus
