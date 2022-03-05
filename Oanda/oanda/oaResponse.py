#import json
import pandas as pd

class oaResponse:
	
	def instrumentResMapToDf(self, instruments):
		#instruments = response.json()
		#print('RESPONSE: ')
		#print(instruments)
		df2 = pd.DataFrame()
		
		if instruments:
			ask = [item['bid'] for item in instruments['candles']]
	
			df = pd.DataFrame(instruments['candles'])
	
			df2 = pd.DataFrame(ask)
	
			df2 = df2.apply(pd.to_numeric)
			df2['time'] = pd.to_datetime(df['time'])
			df2['volume'] = df['volume']
		
		return df2