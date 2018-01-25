#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#IMPORT FLASK
from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session
from flask import redirect
import string
import requests
import sys
import time
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from concurrent.futures import ThreadPoolExecutor, wait

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'


#data base configuration 
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ma_base'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dayenu:secret.word@localhost/dayenu?unix_socket=/usr/local/mysql5/mysqld.sock'

mysql.init_app(app)



def get_ochl(stockID):
    """ Get OCHL Data from the database for one stock
    :param stockID: One stok selected
    :type stockID: int
    :return: OCHL Data of the stock 
    :rtype: DataFrame
    """
    #get the data of every stocks added to the portfolio by the user 
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_getOCHLbyStockID', (stockID,)) #a coder 
    portfolioLinkData = cursor.fetchall()
    cursor.callproc('sp_StockNamebyID', (stockID,)) #a coder 
    stockData = cursor.fetchall()

    """  if len(portfolioLinkData) > 0 and stockData > 0:
        ochlChart = pd.DataFrame.from_dict(portfolioLinkData) #source possible de bugg ici est-ce que data est une liste ou pas? 
        ochlChart.rename(
            columns={'C': 'close', 'H': 'high', 'L': 'low', 'O': 'open', 'T': 'date', 'V': 'volume'},
            inplace=True
        )
        ochlChart['date'] = pd.to_datetime(ochlChart['date'])
        # 18 days * 1 -> 18 ticks
        ochlChart = ochlChart.tail(18)
        ochlChart.set_index(['date'], inplace=True)
        stockName = stockData['Name']
        return stockName, ochlChart

    else:
        return render_template('error.html',error = 'caca')
        print("caca") """

def returns(ochlChart):
    """Compute the returns from a period to the next
    :param df:  OCHL Data
    :type df: DataFrame
    :return:
    """
    ReturnsDataframe = ochlChart.copy()
    ReturnsDataframe.fillna(method='ffill', inplace=True)
    ReturnsDataframe.fillna(method='bfill', inplace=True)
    ReturnsDataframe[1:] = (ochlChart/ochlChart.shift(1)) - 1
    ReturnsDataframe.ix[0, :] = 0
    return ReturnsDataframe

def rand_weights(n):
    """ Initiate an array of random weigths summed to 1.0
    :param n: Array length
    :type n: int
    :return: Array of random weigths
    :rtype: ndarray of float
    """
    weights = np.random.rand(n)
    return weights / np.sum(weights)

def evaluate_portefolio(wei, returns_vec):
    """ Given a repartition, compute expected return and risk from a portefolio

    :param wei: Weights for each currency
    :type wei: ndarray of float
    :return: expected return and risk
    :rtype: (float, float)
    """
    p = np.asmatrix(np.mean(returns_vec, axis=1))
    w = np.asmatrix(wei)
    c = np.asmatrix(np.cov(returns_vec))
    mu = w * p.T
    sigma = np.sqrt(w * c * w.T)
    return mu, sigma

def markowitz_optimization(historical_statuses, evaluate=False):
    """ Construct efficient Markowitz Portefolio
    :param historical_statuses: 18 days OCHL of at least two stocks
    :param eval: evaluate 1000 random portefolios
    :returns: weights, means, stds, opt_mean, opt_std
    TODO : implement short selling (numeric instability w/ constraints)
    """
    nb_stocks = len(historical_statuses)
    lowest_size = np.min([i['close'].size for i in historical_statuses])
    returns_vec = [returns(singlestock)['close'].tail(lowest_size).values for singlestock in historical_statuses]



    def optimal_portfolio():
        def con_sum(t):
            # Short ? -> np.sum(np.abs(t))-1
            return np.sum(t) - 1

        def con_no_short(t):
            # Short support ? add constraint for all weight > 0 to force non short
            # Minimizer instability with constraint_sum !!
            pass

        def quadra_risk_portefolio(ws):
            ws = np.asmatrix(ws)
            c = np.asmatrix(np.cov(returns_vec))
            return ws * c * ws.T

        cons = [{'type': 'eq', 'fun': con_sum}, ]
        # Short ? add no_short constraint  -> cons.append...
        res = minimize(
            quadra_risk_portefolio,
            rand_weights(nb_stocks),
            method='SLSQP',
            constraints=cons,
            options={'disp': False, 'ftol':1e-16,}
        )
        return res.x

    if evaluate:
        n_portfolios = 1000
    else:
        n_portfolios = 1
    means, stds = np.column_stack([
        evaluate_portefolio(rand_weights(nb_stocks), returns_vec)
        for _ in range(n_portfolios)
    ])

    #weights = opt2(returns_vec).flatten() #imal_portfolio()
    weights = optimal_portfolio()
    opt_mean, opt_std = evaluate_portefolio(weights, returns_vec)
    return weights, means, stds, opt_mean, opt_std

def optimiz(stockID):
    """ optimisation 
    :param stockID : list of int
    :returns: weights, means, stds, opt_mean, opt_std
    TODO : implement short selling (numeric instability w/ constraints)
    """
    stocks = sorted(stocks)
    if len(stocks) < 2 or len(stocks) > 10:
        return {"error": "2 to 10 stocks"}
    else:
        """max_workers = 4 if sys.version_info[1] < 5 else None
        executor = ThreadPoolExecutor(max_workers)
        data = dict(future.result() for future in wait([executor.submit(get_ochl, stockID) for stockID in stocks]).done)
        data = [data[stockID] for stockID in stocks]
        errors = [x['error'] for x in data if 'error' in x]
        if errors:
        return {"error": "Stocks not found : " + str(errors)}
        weights, m, s, a, b = markowitz_optimization(data, debug)
        result = dict()
        for i, stockID in enumerate(stocks):
        result[stockID] = weights[i] # faire procedure updatant les weights 
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_updateWeights', (stockID,)) #a coder 
        data = cursor.fetchall()
        """
        return render_template('error.html',error = 'portfolio updated')
