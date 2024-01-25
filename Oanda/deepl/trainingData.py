from sma import Sma
from slope import Slope
from oanda.oaResponse import oaResponse
from itertools import combinations
import numpy as np
#import pandas as pd

# based on real experience
DEFAULT_STEEP_AND_R_VALUE = {
	10: (0.005, 0.7),
	20: (0.015, 0.8),
	30: (0.015, 0.7),
	60: (0.015, 0.8),
	90: (0.02, 0.8)
}

class TrainingData:
	BID_L = 'bid_l'
	ASK_H = 'ask_h'
	PRICE_SLOPE = '_priceSlope_'
	steep_and_r = {}
	
	def buildSmaColName(self, period, col_name):
		return ('sma_' + str(period) + '_' + col_name)
		
	def getSteep(self, period):
		return self.steep_and_r.get(period)[0]
		
	def getSteepR(self, period):
		return self.steep_and_r.get(period)[1]

	def makeTrainingData(self, trading_data, sma_periods = [200, 50, 20], trend_periods = [10, 20, 30, 60, 90], column = 'bid_c', steep_and_r = DEFAULT_STEEP_AND_R_VALUE):
		sma = Sma(trading_data)
		slope = Slope(trading_data)	
		self.steep_and_r = steep_and_r
		
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
		 
		
# Bid Low is the lowest price at which a transaction has been or could have  been completed
# and also Ask High is the highest price at which a transaction has been or could have  been completed
		
		
		values = [1, -1, 0]
		
		for i in trend_periods:
			ask_h_conditions = []
			bid_l_conditions = []
#			values = []
		
			self.training_data = slope.addTrendSlopes(self.ASK_H, i, self.ASK_H + self.PRICE_SLOPE + str(i), startFromFirst = True)
			self.training_data = slope.addTrendSlopes(self.BID_L, i, self.BID_L + self.PRICE_SLOPE + str(i), startFromFirst = True)

			ask_h_price_trend = self.training_data[self.ASK_H + self.PRICE_SLOPE + str(i) + '_roll_ols']
			ask_h_price_trend_r = self.training_data[self.ASK_H + self.PRICE_SLOPE + str(i) +  '_roll_ols_r']
			
			bid_l_price_trend = self.training_data[self.BID_L + self.PRICE_SLOPE + str(i) + '_roll_ols']
			bid_l_price_trend_r = self.training_data[self.BID_L + self.PRICE_SLOPE + str(i) + '_roll_ols_r']


			ask_h_conditions.append((ask_h_price_trend >= self.getSteep(i)) & (ask_h_price_trend_r >= self.getSteepR(i)))
			ask_h_conditions.append((ask_h_price_trend <= (-1) * self.getSteep(i)) & (ask_h_price_trend_r >=  self.getSteepR(i)))
			ask_h_conditions.append(ask_h_price_trend_r <  self.getSteepR(i))
			
			bid_l_conditions.append((bid_l_price_trend >= self.getSteep(i)) & (bid_l_price_trend_r >= self.getSteepR(i)))
			bid_l_conditions.append((bid_l_price_trend <= (-1) * self.getSteep(i)) & (bid_l_price_trend_r >=  self.getSteepR(i)))
			bid_l_conditions.append(bid_l_price_trend_r <  self.getSteepR(i))
			
			self.training_data['ask_h_label_' + str(i)] = np.select(ask_h_conditions, values)
			self.training_data['bid_l_label_' + str(i)] = np.select(bid_l_conditions, values)
			
		return self.training_data