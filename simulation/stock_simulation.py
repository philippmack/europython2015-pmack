__author__ = 'pmack'

def stock_simulation_rule(stock_yesterday,sales,incoming):
    stock = stock_yesterday + incoming
    stock_virtual = max(0,stock - min(stock,sales))
    missing = max(0, sales - stock)
    surplus =max(0, stock-sales)
    return stock_virtual, missing, surplus
