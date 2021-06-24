#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import copy
import time
from kiteconnect import KiteConnect,KiteTicker,exceptions
import sys
import random
import numpy as np
import statistics as stat
import multiprocessing
from multiprocessing import Process ,Queue
import os
import datetime
import traceback
import pandas as pd
import sklearn
from sklearn import *
import tensorflow as tf
import pyspark
#import talib
import json
import math
import requests
import socket
#import matplotlib
import datetime as dt
import urllib.request
from hyperopt import Trials, STATUS_OK, tpe, fmin, hp,SparkTrials
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
############################################################
# gpu_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpu_devices[0], True)
INPUT_PATH = os.path.join("inputs")
OUTPUT_PATH = os.path.join("outputs")
LOG_PATH = OUTPUT_PATH
LOG_FILE_NAME_PREFIX = "stock_pred_lstm_"
LOG_FILE_NAME_SUFFIX = ".log"
##########################################################
class LogMetrics(tf.keras.callbacks.Callback):

	def __init__(self, search_params, param, comb_no):
		self.param = param
		self.self_params = search_params
		self.comb_no = comb_no

	def on_epoch_end(self, epoch, logs):
		for i, key in enumerate(self.self_params.keys()):
			logs[key] = self.param[key]
		logs["combination_number"] = self.comb_no
		if(logs.get('loss')<0.005) and (logs.get("val_loss")<0.005) and (logs.get("mean_squared_error")<0.005) and (logs.get("my_metric_fn")<-1e-06):
			print("\nReached best loss of {} and validation loss of {}... so cancelling training sir!!!!!!!!!!!!!!!!".format(logs.get('loss'), logs.get("val_loss")))
			self.model.stop_training = True
			print("Exiting...in 3\n2\n1")
			sys.exit()
def get_readable_ctime():
	return time.strftime("%d-%m-%Y %H_%M_%S")

csv_logger = tf.keras.callbacks.CSVLogger(OUTPUT_PATH + 'log_' + get_readable_ctime() + '.log', append=True)

def trim_dataset(mat, batch_size):
	"""
	trims dataset to a size that's divisible by BATCH_SIZE
	"""
	no_of_rows_drop = mat.shape[0] % batch_size
	if no_of_rows_drop > 0:
		return mat[:-no_of_rows_drop]
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
##########################################################
df=pd.read_csv("remove_data_test_4yrs.csv")
# df.drop(['stok','stod'],inplace=True,axis=1)
df=df[['open','high','low','close','volume','daily_return','cum_daily_return','H-L','C-O','10day_MA','50day_MA','200day_MA','rsi','Williams %R','ma7','ma21','ema_26','ema_12','bb_High','bb_Low','ema','momentum','TR','atr','STX_14_3','UpI','DoI','PosDI','NegDI','true_ADX','MACD','signal','ROC','Momentum','CCI','tema','turning_line','standard_line','ichimoku_span1','ichimoku_span2','chikou_span']]
df=df.fillna(method="pad")
df.reset_index(drop=True, inplace=True)
##########################################################
values_a = df.values
###########################################################
scalar=MinMaxScaler(feature_range=(0,1))
scaled=scalar.fit(values_a)
scaleded=scaled.transform(values_a)
scalededed=pd.DataFrame(scaleded)
# print(scalededed)
##########################################################

# def ts(a, look_back, pred_col):
# 	t=a.copy()
# 	t=t.iloc[::-1]
# 	t.reset_index(drop=True, inplace=True)
# 	# t['id']=range(1,len(t)+1)
# 	t=t.iloc[look_back:,:]
# 	# t.set_index('id',inplace=True)
# 	pred_value=a.copy()
# 	pred_value=pred_value.iloc[::-1]
# 	pred_value=pred_value.iloc[:-look_back,pred_col]
# 	pred_value.columns=['Pred']
# 	pred_value=pd.DataFrame(pred_value)
# 	# pred_value['id']=range(1,len(pred_value)+1)
# 	# pred_value.set_index('id',inplace=True)
# 	final_df=pd.concat([t,pred_value],axis=1)
# 	return final_df

def data_dummy():
	return None, None, None, None

def data(batch_size,time_steps,look_back):
	arr_df=scalededed
	arr_df.fillna(0,inplace=True)
	arr_df.reset_index(drop=True,inplace=True)
	df_train, df_test = train_test_split(arr_df, train_size=0.9, test_size=0.1, shuffle=False,random_state=444)
	df_dev,df_test_dev = train_test_split(df_test, train_size=0.5, test_size=0.5, shuffle=False,random_state=444)
	train,dev,test=df_train.values,df_dev.values,df_test_dev.values
	BATCH_SIZE = batch_size
	TIME_STEPS = time_steps
	x_train_ts, y_train_ts = build_timeseries(train, 3, TIME_STEPS)
	x_test_ts, y_test_ts = build_timeseries(test, 3, TIME_STEPS)
	x_dev_ts, y_dev_ts = build_timeseries(dev, 3, TIME_STEPS)
	x_train_ts = trim_dataset(x_train_ts, BATCH_SIZE)
	y_train_ts = trim_dataset(y_train_ts, BATCH_SIZE)
	x_dev_ts = trim_dataset(x_dev_ts, BATCH_SIZE)
	y_dev_ts = trim_dataset(y_dev_ts, BATCH_SIZE)
	x_test_ts = trim_dataset(x_test_ts, BATCH_SIZE)
	y_test_ts = trim_dataset(y_test_ts, BATCH_SIZE)
	return x_train_ts, y_train_ts, x_dev_ts,y_dev_ts,x_test_ts, y_test_ts

###########################################################################################################################################

# search_space = {
#   'batch_size': hp.choice('bs', [32,64,128,256,512,1024]),
#   'look_back': hp.choice('ls', [1]),
#   'time_steps': hp.choice('ts', [1,3,5,10,15,30,60]),
#   #'time_steps': hp.choice('ts', [90]),
#   'lstm1_nodes':hp.choice('units_lsmt1', [10,20,30,40,50,60,70,80,90,100]),
#   'lstm1_dropouts':hp.quniform('dos_lstm1',0.1,0.5,0.1),
#   'lstm1_reg':hp.uniform('dos_lstm1_l2',0,1),
#   'dense1_reg':hp.uniform('dos_dense_1_l2',0,1),
#   'lstm_layers': hp.choice('num_layers_lstm',[
# 	  {
# 		  'layers':'one', 

# 	  },
# 	  {
# 		  'layers':'two',
# 		  'lstm2_nodes':hp.choice('units_lstm2', [10,30,50,60,80,100]),
# 		  'lstm2_dropouts':hp.uniform('dos_lstm2',0.1,0.5),
# 		  'lstm2_reg':hp.uniform('dos_lstm2_l2',0.1,0.5)
# 	  },
# 	  {
# 		  'layers':'three',
# 		  'lstm3_nodes':hp.choice('units_lstm3', [10,30,50,60,80,100]),
# 		  'lstm3_dropouts':hp.quniform('dos_lstm3',0.1,0.5,0.1),  
# 		  'lstm3_reg':hp.uniform('dos_lstm3_l2',0.1,0.5)
# 	  }
# 	  ]),
#   'dense_layers': hp.choice('num_layers_dense',[
# 	  {
# 		  'layers':'one',
# 	  },
# 	  {
# 		  'layers':'two',
# 		  'dense2_nodes':hp.choice('units_dense', [10,30,50,60,80,100]),
# 		  'dense2_dropout':hp.quniform('units_dropout', 0.1,0.5,0.1),
# 		  'dense2_reg':hp.uniform('units_reg', 0,1)
# 	  }
# 	  ]),
#   "lr": hp.quniform('lr',0.0000000001,0.1,0.00000000001),
# 	# "epochs": hp.choice('epochs', [2]),
#   "epochs": hp.choice('epochs', [10,40,80,100,200,300,400,500,600,700,800,900,1000]),
#   "optimizer": hp.choice('optmz',["adam"])
# }

search_space = {
  'batch_size': hp.choice('bs', [64]),
  'look_back': hp.choice('ls', [1]),
  'time_steps': hp.choice('ts', [15]),
  #'time_steps': hp.choice('ts', [90]),
  'lstm1_nodes':hp.choice('units_lsmt1', [100]),
  'lstm1_dropouts':hp.choice('dos_lstm1',[0.4]),
  'lstm1_reg':hp.choice('dos_lstm1_l2',[0.15755128783789363]),
  'dense1_reg':hp.choice('dos_dense_1_l2',[0.6523446364617533]),
  'lstm_layers': hp.choice('num_layers_lstm',[
	  {
		  'layers':'one', 

	  },
# 	  {
# 		  'layers':'two',
# 		  'lstm2_nodes':hp.choice('units_lstm2', [10,30,50,60,80,100]),
# 		  'lstm2_dropouts':hp.uniform('dos_lstm2',0.1,0.5),
# 		  'lstm2_reg':hp.uniform('dos_lstm2_l2',0.1,0.5)
# 	  },
	  {
		  'layers':'three',
		  'lstm3_nodes':hp.choice('units_lstm3', [60]),
		  'lstm3_dropouts':hp.choice('dos_lstm3',[0.3000000000000000004]),  
		  'lstm3_reg':hp.choice('dos_lstm3_l2',[0.1995910527819411])
	  }
	  ]),
  'dense_layers': hp.choice('num_layers_dense',[
	  {
		  'layers':'one',
	  },
# 	  {
# 		  'layers':'two',
# 		  'dense2_nodes':hp.choice('units_dense', [10,30,50,60,80,100]),
# 		  'dense2_dropout':hp.quniform('units_dropout', 0.1,0.5,0.1),
# 		  'dense2_reg':hp.uniform('units_reg', 0,1)
# 	  }
	  ]),
  "lr": hp.choice('lr',[0.00511398785]),
	# "epochs": hp.choice('epochs', [2]),
  "epochs": hp.choice('epochs', [80]),
  "optimizer": hp.choice('optmz',["adam"])
}
#######################################################################################################################################
def my_metric_fn(y_true, y_pred):
	difference = tf.math.subtract(y_pred,y_true)
	return difference

def model_lstm_hyperopt(params):
	#call_backs=LogMetrics()
	print("Trying params:",params)
	batch_size = params["batch_size"]
	time_steps = params["time_steps"]
	look_back = params["look_back"]
	xtrain,ytrain,xdev,ydev,xtest,ytest = data(batch_size,time_steps,look_back)
	lstm_model = tf.keras.Sequential()
	# print('xtrain_shape_2={}'.format(xtrain.shape[2]))
	# (batch_size, timesteps, data_dim)
	lstm_model.add(tf.keras.layers.LSTM(params["lstm1_nodes"], batch_input_shape=(batch_size, time_steps, xtrain.shape[2]), dropout=params["lstm1_dropouts"],
						recurrent_dropout=params["lstm1_dropouts"], stateful=True,return_sequences=True,kernel_regularizer=tf.keras.regularizers.l2(params["lstm1_reg"])
						,kernel_initializer='random_uniform',))  
	# ,return_sequences=True #LSTM params => dropout=0.2, recurrent_dropout=0.2
	if params["lstm_layers"]["layers"] == "two":
		lstm_model.add(tf.keras.layers.LSTM(params["lstm_layers"]["lstm2_nodes"], dropout=params["lstm_layers"]["lstm2_dropouts"], 
						kernel_regularizer=tf.keras.regularizers.l2(params["lstm_layers"]["lstm2_reg"])))
	elif params["lstm_layers"]["layers"] == "three":
		lstm_model.add(tf.keras.layers.LSTM(params["lstm_layers"]["lstm3_nodes"], dropout=params["lstm_layers"]["lstm3_dropouts"], 
						kernel_regularizer=tf.keras.regularizers.l2(params["lstm_layers"]["lstm3_reg"])))
	else:
		lstm_model.add(tf.keras.layers.Flatten())

	if params["dense_layers"]["layers"] == 'two':
		lstm_model.add(tf.keras.layers.Dense(params["dense_layers"]["dense2_nodes"], activation='relu',
						kernel_regularizer=tf.keras.regularizers.l2(params["dense_layers"]["dense2_reg"])))
		lstm_model.add(tf.keras.layers.Dropout(params["dense_layers"]["dense2_dropout"]))
	lstm_model.add(tf.keras.layers.Dense(1, activation='relu',kernel_regularizer=tf.keras.regularizers.l2(params["dense1_reg"])))

	lr = params["lr"]
	epochs = params["epochs"]

	if params["optimizer"] =='adam':
		optimizer = tf.keras.optimizers.Adam(lr=lr)
	elif params["optimizer"] =='rms':
		optimizer = tf.keras.optimizers.RMSprop(lr=lr)

	#lstm_model.compile(loss='mean_squared_error', metrics=["acc",tf.keras.metrics.Precision(),tf.keras.metrics.Recall(),tf.keras.metrics.TruePositives(),tf.keras.metrics.TrueNegatives(),tf.keras.metrics.FalsePositives(),tf.keras.metrics.FalseNegatives()],optimizer=optimizer)  # binary_crossentropy
	lstm_model.compile(loss=tf.keras.losses.MeanAbsoluteError(), metrics=[tf.keras.metrics.Poisson(),tf.keras.metrics.RootMeanSquaredError(),tf.keras.metrics.MeanSquaredError(), my_metric_fn],optimizer=optimizer)
	# lstm_model.compile(loss=simple(Loss), metrics=[tf.keras.metrics.Poisson(),tf.keras.metrics.RootMeanSquaredError(),tf.keras.metrics.MeanSquaredError()],optimizer=optimizer)

	
	csv_logger = tf.keras.callbacks.CSVLogger(os.path.join( 'example_from_ashutosh_hyperopt' + '.log'), append=True)
######################################################################################################################################################
#   with tf.device('/GPU:0')
	history=lstm_model.fit(xtrain,ytrain,epochs=epochs,batch_size=batch_size,validation_data=(xdev,ydev),verbose=2,callbacks=[LogMetrics(search_space, params, -1), csv_logger])
	val_error = np.amin(history.history['val_loss'])
	# accuracy= np.amax(history.history['accuracy'])
	# #precision_key=list(history.history.keys())[2]
	# recall_key=list(history.history.keys())[2]
	# TP_key=list(history.history.keys())[3]
	# TN_key=list(history.history.keys())[4]
	# FP_key=list(history.history.keys())[5]
	# FN_key=list(history.history.keys())[6]
	# #print("Precision_key={}".format(precision_key))
	# print("recall_key={}".format(recall_key))
	# #precision=np.amax([history.history[precision_key]])
	# recall=np.amax([history.history[recall_key]])
	# TP=np.amax([history.history[TP_key]])
	# TN=np.amax([history.history[TN_key]])
	# FP=np.amax([history.history[FP_key]])
	# FN=np.amax([history.history[FN_key]])
	# epsilon=float(0.00000008)

	#f1_score=(2 * ((precision * recall) / (precision + recall + epsilon)))
	print('Best validation error of epoch:{}'.format(val_error))
	lstm_model.save('./my_model_11_nov_2020_loss_0.02.h5')
	return {'history':history,'loss': val_error,'status': STATUS_OK, 'model': lstm_model}
	
def run_trials():

# 	trials_step = 0# how many additional trials to do after loading saved trials. 1 = save after iteration
# 	max_trials = 1 # initial max_trials. put something small to not have to wait

	
# 	try:  # try to load an already saved trials object, and increase the max
# 		trials = pickle.load(open("my_trials_metrics_as_poisson_and_rmse_21_july.hyperopt", "rb"))
# 		print("Found saved Trials! Loading...")
# 		max_trials = len(trials.trials) + trials_step
# 		print("Rerunning from {} trials to {} (+{}) trials".format(len(trials.trials), max_trials, trials_step))
# 	except:  # create a new trials object and start searching
# 		trials = Trials()
# 		pickle.dump(trials, open("my_trials_metrics_as_poisson_and_rmse_21_july.hyperopt","wb"))

	best = fmin(fn=model_lstm_hyperopt, space=search_space, algo=tpe.suggest, max_evals=1, rstate=np.random.RandomState(413))
	print("Best_validation_error_of_trial={}".format(best))
	
######################################################################################################################################################
while True:
   run_trials()
######################################################################################################################################################


# In[ ]:




