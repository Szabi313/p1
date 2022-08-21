#import json
import pandas as pd
#from datetime import datetime

class oaResponse:
	
	def instrumentResMapToDf(self, instruments):
		print('response begin')
		#instruments = response.json()
		#print('RESPONSE: ')
		#print(instruments)
		df = pd.DataFrame()
		
		df = pd.json_normalize(instruments['candles'])
		df.rename(columns={'bid.c': 'bid_c'}, inplace=True)
		print(df)
		
		df['time'] = pd.to_datetime(df['time'])
		
		df['bid_c'] = pd.to_numeric(df['bid_c'])
		
		#df['year_float'] = df['time'].dt.year + (30 * df['time'].dt.month + df['time'].dt.day) / 365
		
		df['year_float'] = df['time'].dt.year + df['time'].dt.dayofyear /  366
		
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