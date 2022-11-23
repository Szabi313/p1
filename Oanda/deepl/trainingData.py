from sma import Sma
from slope import Slope
from oanda.oaResponse import oaResponse

class TrainingData:

	def makeTrainingData(self, trading_data, sma_periods = [200, 50, 20], trend_periods = [10, 20, 30, 60, 90], column = 'bid_c'):
		sma = Sma(trading_data)
		slope = Slope(trading_data)	
		
		for i in sma_periods:
			divider = i / 10 if i / 10 > 5 else 5
			self.training_data = sma.getSma(i, column)
			self.training_data = slope.addTrendSlopes('sma_' + str(i) + '_' + column, divider, 'slope_' +str(i))
			self.training_data = slope.addCurveSlopes('year_float', 'year_float_T+1', 'sma_' + str(i) + '_' + column, 'slope_' +str(i))
			
		#self.training_data = slope.addSlopes(column, 30, 'priceSlope', startFromFirst = True)
		#self.training_data = slope.addTrendSlopes(column, 30, 'priceSlope', startFromFirst = True)
		
		for i in trend_periods:
			self.training_data = slope.addTrendSlopes('bid_h', i, 'priceSlope_h_' + str(i), startFromFirst = True)
			self.training_data = slope.addTrendSlopes('bid_l', i, 'priceSlope_l_' + str(i), startFromFirst = True)
			
		return self.training_data