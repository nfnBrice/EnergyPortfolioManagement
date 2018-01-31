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


<<<<<<< HEAD
#data base configuration
=======
#data base configuration 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ma_base'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
<<<<<<< HEAD
app.config['MYSQL_DATABASE_PORT'] = 3306
=======
app.config['MYSQL_DATABASE_PORT'] = 8889
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dayenu:secret.word@localhost/dayenu?unix_socket=/usr/local/mysql5/mysqld.sock'

mysql.init_app(app)



def get_ochl(stockID):
    """ Get OCHL Data from the database for one stock
    :param stockID: One stok selected
    :type stockID: int
<<<<<<< HEAD
    :return: OCHL Data of the stock
    :rtype: DataFrame
    """
    #get the data of every stocks added to the portfolio by the user
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        #print(stockID)
        cursor.callproc('sp_getOCHLbyStockID', (stockID,)) #a coder
=======
    :return: OCHL Data of the stock 
    :rtype: DataFrame
    """
    #get the data of every stocks added to the portfolio by the user 
    try: 
        conn = mysql.connect()
        cursor = conn.cursor()
        #print(stockID)
        cursor.callproc('sp_getOCHLbyStockID', (stockID,)) #a coder 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
        ochlChart = cursor.fetchall()
        #print("ochlchart")
        ochlChartList = [ ]
        for each in ochlChart:
            #print(each[1])
            ochlChartList.append(each[1]);

        #print(ochlChartList);
<<<<<<< HEAD
        cursor.callproc('sp_StockNamebyID', (stockID,)) #a coder
=======
        cursor.callproc('sp_StockNamebyID', (stockID,)) #a coder 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
        stockName = cursor.fetchall()

        return ochlChartList

    finally:
<<<<<<< HEAD
        cursor.close()
        conn.close()

    """  if len(portfolioLinkData) > 0 and stockData > 0:
        ochlChart = pd.DataFrame.from_dict(portfolioLinkData) #source possible de bugg ici est-ce que data est une liste ou pas?
=======
        cursor.close() 
        conn.close()

    """  if len(portfolioLinkData) > 0 and stockData > 0:
        ochlChart = pd.DataFrame.from_dict(portfolioLinkData) #source possible de bugg ici est-ce que data est une liste ou pas? 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
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
    means = [ ]
    r= [ ]
<<<<<<< HEAD
    for i in range(0,len(returns_vec)):
=======
    for i in range(0,len(returns_vec)): 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
        r.append(returns_vec[i])
        #returnv=np.array(returns_vec[i])
        means.append(np.mean(returns_vec[i]))

    p = np.asmatrix(means)
    w = np.asmatrix(wei)
    mu = w * p.T
    c = np.asmatrix(np.cov(r))
    sigma = np.sqrt(w * c * w.T)
    return mu, sigma

def markowitz_optimization(returns_vec, evaluate=False):
    """ Construct efficient Markowitz Portefolio
    :param historical_statuses: 18 days OCHL of at least two stocks
    :param eval: evaluate 1000 random portefolios
    :returns: weights, means, stds, opt_mean, opt_std
    TODO : implement short selling (numeric instability w/ constraints)
    """
    nb_stocks = len(returns_vec)
    #print(returns_vec)
<<<<<<< HEAD

=======
 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
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
    means, stds = np.column_stack([
        evaluate_portefolio(rand_weights(nb_stocks), returns_vec)
        for _ in range(1)
    ])

    weights = optimal_portfolio()
    opt_mean, opt_std = evaluate_portefolio(weights, returns_vec)
    return weights, means, stds, opt_mean, opt_std

def optimiz(stocks):
<<<<<<< HEAD
    """ optimisation
=======
    """ optimisation 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
    :param stocks : list of stock id chosen by the user
    :returns: weights, means, stds, opt_mean, opt_std
    TODO : implement short selling (numeric instability w/ constraints)
    """
    conn = mysql.connect()
    cursor = conn.cursor()

    if len(stocks) < 2 or len(stocks) > 10:
        return {"error": "2 to 10 stocks"}
<<<<<<< HEAD

=======
    
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
    else:
        caca2= [ ]
        for stockID in stocks:
            caca2.append(get_ochl(stockID))
<<<<<<< HEAD

        weights, m, s, a, b = markowitz_optimization(caca2, False)
        print(weights)
        i=0;
        for stockID in stocks:
            cursor.callproc('sp_updateWeights', (session['portfolio'], stockID ,weights[i].item())) #a coder
            conn.commit()
            print("2")
=======
        
        weights, m, s, a, b = markowitz_optimization(caca2, False)

        j=0
        y=0
        l=len(stocks)

        while y<len(stocks) :

            if weights[y].item() < 0:

                caca2.remove(get_ochl(stocks[y]))
                stocks.remove(stocks[y])
                weights, m, s, a, b = markowitz_optimization(caca2, False)
                y=-1

            y=y+1


        i=0;
        for stockID in stocks:
            cursor.callproc('sp_updateWeights', (session['portfolio'], stockID ,weights[i].item())) #a coder
            conn.commit() 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
            i=i+1
        return render_template('error.html',error = 'portfolio updated')
