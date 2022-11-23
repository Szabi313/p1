#import json
#import pandas as pd
from pandas import DataFrame, json_normalize, to_datetime, to_numeric
#from datetime import datetime

class oaResponse:
	
	def instrumentResMapToDf(self, instruments):
		print('response begin')
		#instruments = response.json()
		#print('RESPONSE: ')
		#print(instruments)
		df = DataFrame()
		
		bid_ask_cols = ['bid.o', 'bid.h', 'bid.l', 'bid.c', 'ask.o', 'ask.h', 'ask.l', 'ask.c']
		
		new_bid_ask_cols = ['bid_o', 'bid_h', 'bid_l', 'bid_c', 'ask_o', 'ask_h', 'ask_l', 'ask_c']
		
		df = json_normalize(instruments['candles'])
		
		df.rename(columns=dict(zip(bid_ask_cols, new_bid_ask_cols)), inplace=True)
		
		#df.rename(columns={'bid.o': 'bid_o'}, inplace=True)
#		df.rename(columns={'bid.h': 'bid_h'}, inplace=True)
#		df.rename(columns={'bid.l': 'bid_l'}, inplace=True)
#		df.rename(columns={'bid.c': 'bid_c'}, inplace=True)
#		
#		df.rename(columns={'ask.o': 'ask_o'}, inplace=True)
#		df.rename(columns={'ask.h': 'ask_h'}, inplace=True)
#		df.rename(columns={'ask.l': 'ask_l'}, inplace=True)
#		df.rename(columns={'ask.c': 'ask_c'}, inplace=True)
#		print(df)
		
		df['time'] = to_datetime(df['time'])
		
	#	df['bid_c'] = to_numeric(df['bid_c'])
	
		df[new_bid_ask_cols] = df[new_bid_ask_cols].apply(to_numeric, errors = 'coerce')
		
		print(df.dtypes)
		
		
		#df['year_float'] = df['time'].dt.year + (30 * df['time'].dt.month + df['time'].dt.day) / 365
		
		df['year_float'] = df['time'].dt.year + df['time'].dt.dayofyear /  366
		
		df['year_float_T+1'] = df['year_float'].shift(-1)
		
	#	if instruments:
#			ask = [item['bid'] for item in instruments['candles']]
#	
#			df = pd.DataFrame(instruments['candles'])
#	
#			df2 = pd.DataFrame(ask)
#	
#			df2 = df2.apply(pd.to_numeric)
#			df2['time'] = pd.to_datetime(df['time'])
#			df2['volume'] = df['volume']
		
		print('response end')
	#	return df2
		return df
		
#dt = datetime(2022, 1, 1)
#print(dt)