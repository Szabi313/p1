import json
import argparse
import pandas as pd
#from oanda.oaRequest import oaRequest, endPoints
from sma import Sma
from oanda.oaResponse import oaResponse
#from api.api import ApiInterface
from api.oanda import oaRequest, endPoints
import sys
from slope import Slope

request = oaRequest()

parser = argparse.ArgumentParser(
	description = 'Get stream of instrument(s)'
)

parser.add_argument(
	'-i',
	'--instrument',
	type = str,
	default = 'EUR_HUF',
	action = 'store',
	help = 'The name of the instrument position of which to be taken'
)

instNS = parser.parse_args()

if instNS.instrument:
	print(instNS.instrument)
	
#newOrder = request.makeOrder('EUR_HUF')

#newOrder = request.post(
#{
#	endPoints.orders: ''
#},
#data = json.dumps({
#				"order": {
#					"units": "1",
#					"instrument": "EUR_HUF",
#					"timeInForce": "FOK",
#					"type": "MARKET",
#					"positionFill": "DEFAULT"
#				}
#			}),
#)

#newOrder = newOrder.json()
#print('\nORDER:\n')
#print(newOrder)
#print('\n\n')

#trades = request.get(
#	{
#		endPoints.trades: ''
#	}, instrument=instNS.instrument)

trades = request.getTrades(instNS.instrument)
trades = trades.json()
	
for trade in trades['trades']:
	print(trade)
	print('')


instruments = request.get(
	{
		endPoints.instruments: instNS.instrument,
		endPoints.candles: ''
	},
	#instruments = instNS.instrument,
	#'candles': ''
	#True,
	count = 300,
	#price = 'BMA',
	price = 'B',
	#since = '2020-08-09',
	granularity = 'D'
)

res = oaResponse()
df2 = res.instrumentResMapToDf(instruments)

#instruments = instruments.json()

#print(instruments['candles'])

#close = request.closePosition('417', '1')
#close = close.json()
#print('close: ')
#print(close)

#request.put(
#	{
#		endPoints.trades: '408',
#		endPoints.close: ''
#	},
#	data = json.dumps({ 'units': '1'})
#)



#ask = [item['bid'] for item in instruments['candles']]

#df = pd.DataFrame(instruments['candles'])

#df2 = pd.DataFrame(ask)

#df2 = df2.apply(pd.to_numeric)
#df2['time'] = pd.to_datetime(df['time'])
#df2['volume'] = df['volume']

#ask = pd.Series(ask])
df2['one_day'] = df2['o'].shift(-1)

sma = Sma(df2)

df2 = sma.getSma(200, 'c')
df2 = sma.getSma(50, 'c')
df2 = sma.getSma(20, 'c')

slope = Slope(df2)

df2 = slope.addSlopes('sma_200_c', 5, 'slope_200')
df2 = slope.addSlopes('sma_50_c', 5, 'slope_50')
df2 = slope.addSlopes('sma_20_c', 5, 'slope_20')

df2 = slope.addSlopes('c', 10, 'priceSlope', startFromFirst = True)

#print(df2.iloc[-50:, [0, 5, 6, 7, 9]])
print(df2.columns)
#print(df2.index)
print(df2.loc['250':, ['time', 'h', 'l', 'c', 'o', 'slope_200', 'slope_50', 'slope_20', 'priceSlope','priceSlope_r']])

#period = 200
#source_col = 'c'
#source_col_index = df2.columns.get_loc(source_col)
#col_name = 'sma_{}_' + source_col
#col_name = col_name.format(period)



#print(pd.Series([1,2,3,4,5]).mean(axis = 0))
#print(df2.iloc[0 : period , [3]])
#smas = [df2.iloc[i -period : i , [source_col_index]].mean(axis=0) for i in range(period, len(df2) + 1)]


#smas = pd.Series(smas, index = range(period -1, len(df2)))

#if col_name in df2:
#	pass
#	#print(df2.loc[])
#else:
#	df2[col_name] = smas
#	#print(df2.loc[ '2020-08-18 21:00' : ])

#print(df2.loc[df2['time'] > '2020-09-18', ['time', 'c', 'sma_200_c', 'sma_50_c']])
	
#stream = request.get(
#	{
#		endPoints.pricing: '',
#		endPoints.stream: ''
#	},
#	instruments = instNS.instrument,
#	stream = True
#)	




#stream = request.getPriceStream(instNS.instrument)

#for line in stream.iter_lines():
#			lineP = json.loads(line)
#			print(json.dumps(lineP, indent = 4))




transactions = request.get(
{
	endPoints.transactions: '',
	endPoints.sinceid: ''
}, 
#from = 201, 
id = 200)

transactions = transactions.json()
#print(transactions['transactions'][0])

#print(oanda.endPoints.trades)
#sys.path.append( '/storage/emulated/O/Oanda/api')
#sys.path.append( '/storage/emulated/O/Oanda/api/vendors')
#print(sys.path)