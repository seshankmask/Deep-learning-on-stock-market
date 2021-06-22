import kiteconnect
import copy
from kiteconnect import KiteConnect,KiteTicker,exceptions
import re
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import datetime
import copy
import threading
import time
from time import gmtime, strftime,localtime
import sys
import random
import multiprocessing
from multiprocessing import Process ,Queue
import os
import traceback
import pandas as pd
import tensorflow as tf
import pyspark
import talib
import sklearn
import math
import socket
import matplotlib.pyplot as plt
from hyperopt import Trials, STATUS_OK, tpe, fmin, hp,SparkTrials
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import date, timedelta

#Stage2
########################################################################################################################################
batch_size =1024
time_steps =30
look_back =1
# need to give your api_key and api_secret here. You need to request it from Kite api(in my case)
kite = KiteConnect(api_key=api_key)
kite_ticker=KiteTicker(api_key=api_key,access_token=access_token)
# proxies = {
#   'http': 'http://proxy.blisc.in:3128',
#   'https': 'https://proxy.blisc.in:3128',
# }   
kite.__init__(api_key=api_key,timeout=1000000)
kite_ticker.__init__(api_key=api_key,access_token=access_token,reconnect=True,reconnect_max_tries=300,reconnect_max_delay=60,connect_timeout=10000)
kite.set_access_token(access_token)
instrument_token ='128083204'
instrument_token_for_quote =128083204
# from_date = "2020-09-29"
# to_date = "2020-10-02"
# interval = "minute"
######################################################################################################
def get_historical_data():
    # try:
    value= kite.historical_data(instrument_token, from_date, to_date, interval='minute',continuous=0)
    if value!=None:
        return value
    else:
        pass

i=1
df=pd.DataFrame()
to_date = date.today()
from_date = to_date - timedelta(days = 60)
# to_date="{}".format(to)
# from_date="{}".format(form)
while i<=2:
# while i <=30:
    try:
        print(i)
        print(to_date,from_date)
        instrument_token ='128083204'
        instrument_token_for_quote =128083204
        interval = "minute"
        records =get_historical_data()
        px=pd.DataFrame(records)
        px =px.iloc[::-1]
        px=px.iloc[:-1:]
    #     px.reset_index(drop=True)
        df=df.append(px)
        to_date=to_date -timedelta(days=61)
        from_date=to_date-timedelta(days=60)
        i+=1
    except KeyboardInterrupt:
        sys.exit()
    except KeyError:
        time.sleep(3)
        api_key = 'g58hqt19c8htbuw3'
        api_secret="zor78r0jbuow5vxk6jd7w59rhmzwt2gi"
        access_token='6CMIxmt5odOF57cDJqg29Xv6vHC5h6zK'
        # kite = KiteConnect(api_key=api_key)
        # proxies = {
        #   'http': 'http://proxy.blisc.in:3128',
        #   'https': 'https://proxy.blisc.in:3128',
        # }   
        kite.__init__(api_key=api_key,timeout=1000000)
        kite_ticker.__init__(api_key=api_key,access_token=access_token,reconnect=True,reconnect_max_tries=300,reconnect_max_delay=60,connect_timeout=10000)
        kite.set_access_token(access_token)
    except socket.gaierror:
        api_key = 'g58hqt19c8htbuw3'
        api_secret="zor78r0jbuow5vxk6jd7w59rhmzwt2gi"
        access_token='6CMIxmt5odOF57cDJqg29Xv6vHC5h6zK'
        # kite = KiteConnect(api_key=api_key)
        # proxies = {
        #   'http': 'http://proxy.blisc.in:3128',
        #   'https': 'https://proxy.blisc.in:3128',
        # }   
        kite.__init__(api_key=api_key,timeout=1000000)
        kite_ticker.__init__(api_key=api_key,access_token=access_token,reconnect=True,reconnect_max_tries=300,reconnect_max_delay=60,connect_timeout=10000)
        kite.set_access_token(access_token)
    except Exception as f:
        print(f)
        api_key = 'g58hqt19c8htbuw3'
        api_secret="zor78r0jbuow5vxk6jd7w59rhmzwt2gi"
        access_token='6CMIxmt5odOF57cDJqg29Xv6vHC5h6zK'
        # kite = KiteConnect(api_key=api_key)
        # proxies = {
        #   'http': 'http://proxy.blisc.in:3128',
        #   'https': 'https://proxy.blisc.in:3128',
        # }   
        kite.__init__(api_key=api_key,timeout=1000000)
        kite_ticker.__init__(api_key=api_key,access_token=access_token,reconnect=True,reconnect_max_tries=300,reconnect_max_delay=60,connect_timeout=10000)
        kite.set_access_token(access_token)

    except HTTPSConnectionPool as e:
        print(e)
        python=sys.executable
        os.execl(python,python,"./Data_extraction_reliance-checkpoint.py")
        api_key = 'g58hqt19c8htbuw3'
        api_secret="zor78r0jbuow5vxk6jd7w59rhmzwt2gi"
        access_token='6CMIxmt5odOF57cDJqg29Xv6vHC5h6zK'
        # kite = KiteConnect(api_key=api_key)
        # proxies = {
        #   'http': 'http://proxy.blisc.in:3128',
        #   'https': 'https://proxy.blisc.in:3128',
        # }   
        kite.__init__(api_key=api_key,timeout=1000000)
        kite_ticker.__init__(api_key=api_key,access_token=access_token,reconnect=True,reconnect_max_tries=300,reconnect_max_delay=60,connect_timeout=10000)
        kite.set_access_token(access_token)
    except kiteconnect.exceptions:
        api_key = 'g58hqt19c8htbuw3'
        api_secret="zor78r0jbuow5vxk6jd7w59rhmzwt2gi"
        access_token='6CMIxmt5odOF57cDJqg29Xv6vHC5h6zK'
        kite = KiteConnect(api_key=api_key)
        # proxies = {
        #   'http': 'http://proxy.blisc.in:3128',
        #   'https': 'https://proxy.blisc.in:3128',
        # }   
        kite.__init__(api_key=api_key,timeout=1000000)
        kite_ticker.__init__(api_key=api_key,access_token=access_token,reconnect=True,reconnect_max_tries=300,reconnect_max_delay=60,connect_timeout=10000)
        kite.set_access_token(access_token)
        python=sys.executable
        os.execl(python,python,"./Data_extraction_reliance-checkpoint.py")
                


class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):

        if(logs.get("val_loss")<=0.01):
            print("\nReached best loss of {} and validation loss of {}... so cancelling training sir!!!!!!!!!!!!!!!!".format(logs.get('loss'), logs.get("val_loss")))
            self.model.stop_training = True
            print("Exiting...in 3\n2\n1")

def get_readable_ctime():
    return time.strftime("%d-%m-%Y %H_%M_%S")

csv_logger = tf.keras.callbacks.CSVLogger('log_' + get_readable_ctime() + '.log', append=True)

def trim_dataset(mat, batch_size):
    """
    trims dataset to a size that's divisible by BATCH_SIZE
    """
    no_of_rows_drop = mat.shape[0] % batch_size
    if no_of_rows_drop > 0:
        # return mat[:-no_of_rows_drop]
        return mat[no_of_rows_drop:]
    else:
        return mat


def build_timeseries(mat, y_col_index, time_steps):
    # total number of time-series samples would be len(mat) - TIME_STEPS
    dim_0 = mat.shape[0] - time_steps
    dim_1 = mat.shape[1]
    x = np.zeros((dim_0, time_steps, dim_1))
    y = np.zeros((x.shape[0],))

    for i in range(dim_0):
        x[i] = mat[i:time_steps + i]
        y[i] = mat[time_steps + i, y_col_index]
    print("length of time-series i/o {} {}".format(x.shape, y.shape))
    return x, y
# df.reindex(index=df.index[::-1])
# records =get_historical_data()
# df=pd.DataFrame(records)
# df.to_csv("exported_1month_data.csv",header=True)

##################################################################################################################################################
# df=pd.read_csv("exported_1month_data.csv")
main_df= df.copy()
main_df=main_df.reset_index(drop=True)
main_df=main_df.iloc[::-1]
main_df=main_df.reset_index(drop=True)
df=df[['date','open','high','low','close','volume']]
# print(df)

##########################################################################
df['daily_return'] = df.close.pct_change().fillna(0)
df['cum_daily_return'] = (1 + df['daily_return']).cumprod()
df['H-L'] = df.high - df.low
df ['C-O'] = df.close - df.open
df['10day_MA'] = df.close.shift(1).rolling(window = 10).mean().fillna(0)
df['50day_MA'] = df.close.shift(1).rolling(window = 50).mean().fillna(0)
df['200day_MA'] = df.close.shift(1).rolling(window = 200).mean().fillna(0)
df['rsi'] = talib.RSI(df.close.values, timeperiod = 14)
df['Williams %R'] = talib.WILLR(df.high.values,
df.low.values,
df.close.values, 14)
# Create 7 and 21 days Moving Average
df['ma7'] = df.close.rolling(window=7).mean().fillna(0)
df['ma21'] = df.close.rolling(window=21).mean().fillna(0)

# Creating MACD
df['ema_26'] = df.close.ewm(span=26).mean().fillna(0)
df['ema_12'] = df.close.ewm(span=12).mean().fillna(0)
# df['macd'] = (df['ema_12'] - df['ema_26'])
# Creating Bollinger Bands
#Set number of days and standard deviations to use for rolling lookback period for Bollinger band calculation
window = 21
no_of_std = 2
#Calculate rolling mean and standard deviation using number of days set above
rolling_mean = df.close.rolling(window).mean()
rolling_std = df.close.rolling(window).std()
#create two new DataFrame columns to hold values of upper and Lower Bollinger bands
#B[‘Rolling Mean’] = rolling_mean.fillna(0)
df['bb_High'] = (rolling_mean + (rolling_std * no_of_std)).fillna(0)
df['bb_Low'] = (rolling_mean - (rolling_std * no_of_std)).fillna(0)

# Create Exponential moving average
df['ema'] = df.close.ewm(com=0.5).mean()
#Create ADX
# df['ADX']= talib.ADX(df.high.values,df.low.values,df.close.values,timeperiod=14)
# df['ADX'].fillna(0,inplace=True)
# Create Momentum
df['momentum'] = df.close - 1
#############################################################################################
#Calculation of Price Rate of Change
# ROC = [(Close - Close n periods ago) / (Close n periods ago)] * 100
df['ROC'] = ((df['close'] - df['close'].shift(12)) /
(df['close'].shift(12)))*100
df = df.fillna(0)
#Calculation of Momentum
df['Momentum'] = df['close'] - df['close'].shift(4)
df = df.fillna(0)
#Calculation of Commodity Channel Index
tp = (df['high'] + df['low'] + df['close']) / 3
ma = tp / 20
md = (tp - ma) / 20
df['CCI'] = (tp-ma)/(0.015 * md)
# Calculation of Triple Exponential Moving Average
# Triple Exponential MA Formula:
# T-EMA = (3EMA - 3EMA(EMA)) + EMA(EMA(EMA))
# Where:
# EMA = EMA(1) + α * (Close - EMA(1))
# α = 2 / (N + 1)
# N = The smoothing period.
df['ema'] = df['close'].ewm(span=3,min_periods=0,adjust=True,ignore_na=False).mean()
df = df.fillna(0)
df['tema'] = (3 * df['ema'] - 3 * df['ema'] * df['ema']) + (df['ema'] *
df['ema'] *
df['ema'])
# Turning Line
high = df['high'].rolling(window=9,center=False).max()
low = df['low'].rolling(window=9,center=False).min()
df['turning_line'] = (high + low) / 2
# Standard Line
p26_high = df['high'].rolling(window=26,center=False).max()
p26_low = df['low'].rolling(window=26,center=False).min()
df['standard_line'] = (p26_high + p26_low) / 2
# Leading Span 1
df['ichimoku_span1'] = ((df['turning_line'] + df['standard_line']) / 2).shift(26)

# Leading Span 2
p52_high = df['high'].rolling(window=52,center=False).max()
p52_low = df['low'].rolling(window=52,center=False).min()
df['ichimoku_span2'] = ((p52_high + p52_low) / 2).shift(26)

# The most current closing price plotted 22 time periods behind (optional)
df['chikou_span'] = df['close'].shift(-22) # 22 according to investopedia
##################################################################################
#My indicators
def EMA(df, base, target, period, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)
    
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)
        
    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat([df[:period][base].rolling(window=period).mean(), df[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df

def ATR(df, period, ohlc=['Open', 'High', 'Low', 'Close']):
    """
    Function to compute Average True Range (ATR)
    
    Args :
        df : Pandas DataFrame which contains ['date', 'Open', 'High', 'Low', 'Close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
        
    Returns :
        df : Pandas DataFrame with new columns added for 
            True Range (TR)
            ATR (ATR_$period)
    """
    atr = 'ATR_' + str(period)

    # Compute true range only if it is not computed and stored earlier in the df
    if not 'TR' in df.columns:
        df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
        df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
        df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())
         
        df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)
         
        df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(df, 'TR', 'atr', period, alpha=True)
    df.drop(['TR'],axis=1)
    return df

def SuperTrend(df, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close']):
    """
    Function to compute SuperTrend
    
    Args :
        df : Pandas DataFrame which contains ['date', 'Open', 'High', 'Low', 'Close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the ATR
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
        
    Returns :
        df : Pandas DataFrame with new columns added for 
            True Range (TR), ATR (ATR_$period)
            SuperTrend (ST_$period_$multiplier)
            SuperTrend Direction (STX_$period_$multiplier)
    """

    ATR(df, period, ohlc=ohlc)
    atr = 'ATR_' + str(period)
    st = 'ST_' + str(period) + '_' + str(multiplier)
    stx = 'STX_' + str(period) + '_' + str(multiplier)
    
    
    """
    SuperTrend Algorithm :
    
        BASIC UPPERBAND = (High + Low) / 2 + Multiplier * ATR
        BASIC LowERBAND = (High + Low) / 2 - Multiplier * ATR
        
        FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                            THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
        FINAL LowERBAND = IF( (Current BASIC LowERBAND > Previous FINAL LowERBAND) or (Previous Close < Previous FINAL LowERBAND)) 
                            THEN (Current BASIC LowERBAND) ELSE Previous FINAL LowERBAND)
        
        SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                        Current FINAL UPPERBAND
                    ELSE
                        IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                            Current FINAL LowERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL LowERBAND) and (Current Close >= Current FINAL LowERBAND)) THEN
                                Current FINAL LowERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LowERBAND) and (Current Close < Current FINAL LowERBAND)) THEN
                                    Current FINAL UPPERBAND
    """
    # Compute basic upper and Lower bands
    # print(df[atr])
    df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df['atr']
    df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df['atr']
    # Compute final upper and Lower bands
    df['final_ub'] = 0.00
    df['final_lb'] = 0.00
    for i in range(period, len(df)):
        df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i - 1] or df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else df['final_ub'].iat[i - 1]
        df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i - 1] or df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else df['final_lb'].iat[i - 1]
       
    # Set the Supertrend value
    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] <= df['final_ub'].iat[i] else \
                        df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] >  df['final_ub'].iat[i] else \
                        df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= df['final_lb'].iat[i] else \
                        df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] <  df['final_lb'].iat[i] else 0.00 
                 
    # Mark the trend direction up/down
#     df[stx] = np.where((df[st] > 0.00), np.where((df[ohlc[3]] < df[st]), 'down',  'up'), np.NaN)
    df[stx] = df[st]
    # Remove basic and final bands from the columns
    df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb',st], inplace=True, axis=1)
    
    df.fillna(0, inplace=True)

    return df


def get_ADX(df, n, n_ADX):
    """Calculate the Average Directional Movement Index for given data.
    
    :param px: pandas.DataFrame
    :param n: 
    :param n_ADX: 
    :return: pandas.DataFrame
    """

    i = 0
    UpI = []
    DoI = []
    while i+1<= df.index[-1]:
        UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
        DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = df['atr']
    df['upi'] = pd.Series(UpI)
    df['doi'] = pd.Series(DoI)
    EMA(df=df, base='upi', target='UpI', period=14, alpha=True)
    EMA(df=df, base='doi', target='DoI', period=14, alpha=True)
    df['posdi']=df['UpI']/df['atr']
    df['negdi']=df['DoI']/df['atr']
    EMA(df=df, base='posdi', target='PosDI', period=14, alpha=True)
    EMA(df=df, base='negdi', target='NegDI', period=14, alpha=True)
    df['adx']= abs((df['posdi'] - df['negdi'])/(df['posdi'] + df['negdi']))
    EMA(df,'adx', 'true_ADX', period=14, alpha=True)
    df.drop(['adx', 'posdi', 'negdi', 'upi','doi'], inplace=True, axis=1)
    return df

def get_MACD(df) :
    close_12_ewma=df['close'].ewm(span=12, min_periods=0, adjust=True, ignore_na=True).mean()
    close_26_ewma=df['close'].ewm(span=26, min_periods=0, adjust=True, ignore_na=True).mean()
    # px['26ema'] = px['26ema'].reindex_like(px,method='ffill')
    df['26ema'] = close_26_ewma
    df['12ema'] = close_12_ewma
    df['MACD'] = round((df['12ema'] - df['26ema']),3)
    df['signal'] = df['MACD'].ewm(span=9, min_periods=0, adjust=True, ignore_na=True).mean()
    df.drop(['26ema','12ema'], inplace=True, axis =1)
    return df

def stok(df,n):
    df['stok'] = ((df['close']-df['low'].rolling(window=n,center=False,).mean())/(df['high'].rolling(window=n,center=False,).max() - df['low'].rolling(window=n,center=False,).min()))*100
    df['stod'] = df['stok'].rolling(window=n,center=False,).mean()
    return df

def news_api():
    ny_times = ('https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=Lq2MwaHUecj8voxGj6SwXnhg31dNTGtJ')
    resp_ny_times= requests.get(business_news_url_in)
    data_top_HL_ny_times=resp.json()
    data_ny_times=data_top_HL_ny_times['results'][0]['abstract']
    business_news_url_in = ('http://newsapi.org/v2/top-headlines?country=in&sortBy=publishedAt&category=business&apiKey=d0273c0c1b134f7282ab910758c79c46')
    resp= requests.get(business_news_url_in)
    data_top_HL=resp.json()
    data_business=list(data_top_HL['articles'])[0]
    reliance_url = ('http://newsapi.org/v2/everything?q=reliance&from=2020-06-16&to=2020-06-16&sortBy=publishedAt&apiKey=d0273c0c1b134f7282ab910758c79c46')
    resp_reliance= requests.get(reliance_url)
    data_top_rel=resp_reliance.json()
    data_rel=list(data_top_rel['articles'])[0]
    try:
        ana_ny_times = SentimentIntensityAnalyzer()
        vs_ny_times = ana_sentence.polarity_scores(data_top_HL_ny_times)
        ##############################################
        sentences_buss=[data_business['description']]
        ana_buss=SentimentIntensityAnalyzer()
        vs_buss = ana_buss.polarity_scores(sentences_buss)
        buss_time=data_business['publishedAt']
        sentences_rel=[data_rel['description']]
        ana_rel=SentimentIntensityAnalyzer()
        vs_rel = ana_rel.polarity_scores(sentences_rel)
        rel_time=data_rel['publishedAt']
      ######################################################
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass
    return sentences_buss,vs_buss,buss_time,sentences_rel,vs_rel,rel_time,vs_ny_times

def mmi():
    try:
        url="https://www.tickertape.in/market-mood-index"
        page=requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results=soup.find(id='__NEXT_DATA__')
        links_dict = json.loads(results.string)
        time_sec=links_dict['props']['pageProps']['nowData']['date'].split("T")[1].split("Z")[0].split(".")[0].split(":")[1] 
        current_MMI=links_dict['props']['pageProps']['nowData']['currentValue']
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass
    return current_MMI
#######################################################################################################
# df=df.reset_index(drop=True)
# df=df.iloc[::-1]
# df=df.reset_index(drop=True)
df=ATR(df=df, period=14, ohlc=['open', 'high', 'low', 'close'])
                    
df=SuperTrend(df=df, period=14, multiplier=3, ohlc=['open', 'high', 'low', 'close'])
# print(df)
df=get_ADX(df=df,n=14,n_ADX=14)
df =get_MACD(df)
df=stok(df,4)
df=df[['open','high','low','close','volume','daily_return','cum_daily_return','H-L','C-O','10day_MA','50day_MA','200day_MA','rsi','Williams %R','ma7','ma21','ema_26','ema_12','bb_High','bb_Low','ema','momentum','TR','atr','STX_14_3','UpI','DoI','PosDI','NegDI','true_ADX','MACD','signal','ROC','Momentum','CCI','tema','turning_line','standard_line','ichimoku_span1','ichimoku_span2','chikou_span']]


# df.to_csv("remove_one_month_data.csv",header=True,index=False)
# print(df)

######################################################################################################
# f=pd.read_csv("remove_data_test_2months.csv")
df = f.append(df)
print(df)
# df.drop(['stok','stod'],inplace=True,axis=1)
# df=df[['open','high','low','close','volume','daily_return','cum_daily_return','H-L','C-O','10day_MA','50day_MA','200day_MA','rsi','Williams %R','ma7','ma21','ema_26','ema_12','bb_High','bb_Low','ema','momentum','TR','atr','STX_14_3','UpI','DoI','PosDI','NegDI','true_ADX','MACD','signal','ROC','Momentum','CCI','tema','turning_line','standard_line','ichimoku_span1','ichimoku_span2','chikou_span']]
# df=df[['open','high','low','close','volume','daily_return','cum_daily_return','H-L','C-O','10day_MA','50day_MA','200day_MA','rsi','Williams %R','ma7','ma21','ema_26','ema_12','bb_High','bb_Low','ema','momentum','TR','atr','STX_14_3','UpI','DoI','PosDI','NegDI','true_ADX','MACD','signal','ROC','Momentum','CCI','tema','turning_line','standard_line','ichimoku_span1','ichimoku_span2','chikou_span']]
# df=df.iloc[::-1]
df=df.fillna(method="pad")
df.reset_index(drop=True, inplace=True)
######################################################################################################
values_a = df.values
values_a_y=pd.DataFrame(df['open'].tolist()).to_numpy()
######################################################################################################
scalar=MinMaxScaler(feature_range=(0,1))
scaled=scalar.fit(values_a)
scaleded=scaled.transform(values_a)
scalededed=pd.DataFrame(scaleded)
# print(scalededed)
scalar_y=MinMaxScaler(feature_range=(0,1))
scaled_y=scalar_y.fit(values_a_y)
scaleded_y=scaled_y.transform(values_a_y)
scalededed_y=pd.DataFrame(scaleded_y)
##########################################################

def ts(a, look_back, pred_col):
    t=a.copy()
    t=t.iloc[::-1]
    t.reset_index(drop=True, inplace=True)
    # t['id']=range(1,len(t)+1)
    t=t.iloc[look_back:,:]
    # t.set_index('id',inplace=True)
    pred_value=a.copy()
    pred_value=pred_value.iloc[::-1]
    pred_value=pred_value.iloc[:-look_back,pred_col]
    pred_value.columns=['Pred']
    pred_value=pd.DataFrame(pred_value)
    # pred_value['id']=range(1,len(pred_value)+1)
    # pred_value.set_index('id',inplace=True)
    final_df=pd.concat([t,pred_value],axis=1)
    return final_df

def data_dummy():
    return None, None, None, None

def data(batch_size,time_steps,look_back):
    arr_df=ts(scalededed,look_back,0)
    arr_df.fillna(0,inplace=True)
    arr_df.reset_index(drop=True,inplace=True)
    # df_train, df_test = train_test_split(arr_df, train_size=0.9, test_size=0.1, shuffle=False,random_state=444)
    # df_dev,df_test_dev = train_test_split(df_test, train_size=0.5, test_size=0.5, shuffle=False,random_state=444)
    # train,dev,test=df_train.values,df_dev.values,df_test_dev.values
    train=arr_df.values
    BATCH_SIZE = batch_size
    TIME_STEPS = time_steps
    x_train_ts, y_train_ts = build_timeseries(train, 0, TIME_STEPS)
    # print(test)
    # x_test_ts, y_test_ts = build_timeseries(test, 0, TIME_STEPS)
    # print('YESSSSSSSSSSSSSSSSSSSSSSSSSS')
    # x_dev_ts, y_dev_ts = build_timeseries(dev, 0, TIME_STEPS)
    x_train_ts = trim_dataset(x_train_ts, BATCH_SIZE)
    y_train_ts = trim_dataset(y_train_ts, BATCH_SIZE)
    # x_dev_ts = trim_dataset(x_dev_ts, BATCH_SIZE)
    # y_dev_ts = trim_dataset(y_dev_ts, BATCH_SIZE)
    # x_test_ts = trim_dataset(x_test_ts, BATCH_SIZE)
    # y_test_ts = trim_dataset(y_test_ts, BATCH_SIZE)
    return x_train_ts, y_train_ts

def my_metric_fn(y_true, y_pred):
    difference = tf.math.subtract(y_pred,y_true)
    return difference

def get_quotes(quote):
    try:
        quotes = kite.quote(instrument_token)
        quote.put_nowait(quotes)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        python=sys.executable
        os.execl(python,python,"testing_model_post_hyperopting_round2.py")
# callbacks=myCallback()

################################################################################################################################################################


xtrain,ytrain = data(batch_size,time_steps,look_back)
print(xtrain.shape)
print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
###################################################################################################################################################
dependencies = {
    'my_metric_fn': my_metric_fn}

lstm_model=tf.keras.models.load_model("/Volumes/Reserved/Deep_learning/LSTM_implement_ashutosh_example/best_model.h5", custom_objects=dependencies)
y_pred=lstm_model.predict(x=xtrain,batch_size=1024,use_multiprocessing=True)
y_pred_transformed=scalar_y.inverse_transform(y_pred)
print(y_pred_transformed[0:20])
# main_df.iloc[:,0],y_pred_transformed
########################################################################################################################################################
# plt.plot(main_df.iloc[:,0],y_pred_transformed)
# plt.show()

# def start():
#   t1 = t2 = t3 = 0
#   period1 = 1.0 # do function1() every second
#   period2 = 60.0  # do function2() every hour
#   period3 = 6.0
#   sleep_seconds = 0.1# or whatever makes sense
#   # t=time.time()
#   while True:
#       t = time.time()
#       print(t)
#       if t - t1 >= period1:
#           records=get_historical_data()
#           fd=records[-1]['date'].time()
#           # time=strftime("%H:%M:%S", localtime())
#           print(fd)
#           t1 = time.time()

#       if t - t2 >= period2:
#           sentences_buss,vs_buss,buss_time,sentences_rel,vs_rel,rel_time,vs_ny_times=news_api()
#           print("Business_news_now={}".format(sentences_buss))
#           print("Business_news_sentiment={}".format(vs_buss['compound']))
#           print("Business_news_time={}".format(buss_time))
#           print("############################################")
#           print("Reliance_news_now={}".format(sentences_rel))
#           print("Reliance_news_sentiment={}".format(vs_rel['compound']))
#           print("Reliance_news_time={}".format(rel_time))
#           print("############################################")
#           t2 = time.time()

#       if t - t3 >= period3:
#           current_MMI  = mmi()
#           print("current_MMI={}".format(current_MMI))
#           print("############################################")
#           t3= time.time()

#       time.sleep(sleep_seconds)
#       # threading.Timer(120, news_MMI).start()
        

# start()
