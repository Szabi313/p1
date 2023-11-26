from sma import Sma
from slope import Slope
from oanda.oaResponse import oaResponse
from itertools import combinations

# based on real experience
DEFAULT_STEEP_AND_R_VALUE = {
	10: (0.005, 0.7),
	20: (0.015, 0.8),
	30: (0.015, 0.7)
}

class TrainingData:
	BID_L = 'bid_l'
	ASK_H = 'ask_h'
	
	def buildSmaColName(self, period, col_name):
		return ('sma_' + str(period) + '_' + col_name)

	def makeTrainingData(self, trading_data, sma_periods = [200, 50, 20], trend_periods = [10, 20, 30, 60, 90], column = 'bid_c'):
		sma = Sma(trading_data)
		slope = Slope(trading_data)	
		
		for i in sma_periods:
			divider = i / 10 if i / 10 > 5 else 5
			self.training_data = sma.getSma(i, column)
			self.training_data = slope.addTrendSlopes(self.buildSmaColName(i, column), divider, 'slope_' +str(i))
			self.training_data = slope.addCurveSlopes('year_float', 'year_float_T+1', self.buildSmaColName(i, column), 'slope_' +str(i))
			
		smas_and_prices = sma_periods.copy()
		smas_and_prices.append(self.BID_L)
		smas_and_prices.append( self.ASK_H)
	
		sma_price_combinations = list(combinations(smas_and_prices, 2))
		print(sma_price_combinations)
		
		for pair in sma_price_combinations:
			pair = tuple(pair)
			
			if pair[0] != self.BID_L and pair[0] != self.ASK_H:
				self.training_data['sma_' + str(pair[0]) + '_per_' + str(pair[1])] = self.training_data[self.buildSmaColName(pair[0], column)] /( self.training_data[self.buildSmaColName(pair[1], column)] if pair[1] != self.ASK_H and pair[1] != self.BID_L else self.training_data[str(pair[1])])
			
			
	#		for elem in tuple(pair):
	#			print(elem)
		 
			
		#self.training_data = slope.addSlopes(column, 30, 'priceSlope', startFromFirst = True)
		#self.training_data = slope.addTrendSlopes(column, 30, 'priceSlope', startFromFirst = True)
		
# Bid Low is the lowest price at which a transaction has been or could have  been completed
# and also Ask High is the highest price at which a transaction has been or could have  been completed
		
		for i in trend_periods:
			self.training_data = slope.addTrendSlopes('ask_h', i, 'priceSlope_h_' + str(i), startFromFirst = True)
			self.training_data = slope.addTrendSlopes('bid_l', i, 'priceSlope_l_' + str(i), startFromFirst = True)
			
		return self.training_data